import io
from unittest import mock
from unittest.mock import Mock

from django.core.management import call_command
from django.test import TestCase, override_settings


def _mock_part(pk, on_hand, reorder_point, needs_reorder, supplier_id=10, reorder_quantity=3):
    return Mock(
        pk=pk, part_id=pk, on_hand=on_hand, reorder_point=reorder_point,
        needs_reorder=needs_reorder, supplier_id=supplier_id, reorder_quantity=reorder_quantity,
        part_description='Widget',
    )


class ScanReorderAlertsCommandTests(TestCase):
    def _run(self, parts, drafted_orders=None):
        """
        Parts.objects.filter() is called twice for different purposes in the command:
        once to fetch all parts with a reorder_point set, and once per part to persist
        an updated needs_reorder flag. A flat return_value can't distinguish those calls
        (the second would return the same list, which has no .update()), so route by
        call signature and hand back a fresh per-pk mock for the update calls.
        """
        out = io.StringIO()
        update_mocks = {}

        def filter_side_effect(**kwargs):
            if 'reorder_point__isnull' in kwargs:
                return parts
            update_mock = Mock()
            update_mocks[kwargs['pk']] = update_mock
            return update_mock

        with mock.patch('apps.inventory.management.commands.scan_reorder_alerts.Parts') as MockParts, \
                mock.patch(
                    'apps.inventory.management.commands.scan_reorder_alerts.'
                    'draft_purchase_orders_from_reorder_alerts',
                    return_value=drafted_orders or [],
                ) as mock_draft, \
                mock.patch(
                    'apps.inventory.management.commands.scan_reorder_alerts.send_mail'
                ) as mock_send_mail:
            MockParts.objects.filter.side_effect = filter_side_effect
            call_command('scan_reorder_alerts', stdout=out)
        return out.getvalue(), update_mocks, mock_draft, mock_send_mail

    def test_part_crossing_threshold_is_flagged_and_persisted(self):
        part = _mock_part(pk=1, on_hand=2, reorder_point=5, needs_reorder=0)
        output, update_mocks, mock_draft, _ = self._run([part])

        self.assertIn('1 newly flagged', output)
        update_mocks[1].update.assert_called_once_with(needs_reorder=1)
        mock_draft.assert_called_once_with([part])

    def test_part_already_flagged_is_not_recounted(self):
        part = _mock_part(pk=1, on_hand=2, reorder_point=5, needs_reorder=1)
        output, _, mock_draft, _ = self._run([part])

        self.assertIn('0 newly flagged', output)
        mock_draft.assert_not_called()

    def test_part_above_threshold_stays_unflagged(self):
        part = _mock_part(pk=1, on_hand=10, reorder_point=5, needs_reorder=0)
        output, _, mock_draft, _ = self._run([part])

        self.assertIn('0 newly flagged', output)
        mock_draft.assert_not_called()

    @override_settings(REORDER_ALERT_RECIPIENTS=['owner@example.com'])
    def test_sends_email_digest_when_recipients_configured(self):
        part = _mock_part(pk=1, on_hand=2, reorder_point=5, needs_reorder=0)
        drafted_po = Mock(pk=99, supplier=Mock(supplier_name='Acme'))
        output, _, _, mock_send_mail = self._run([part], drafted_orders=[drafted_po])

        mock_send_mail.assert_called_once()
        self.assertIn('Sent low-stock digest', output)
        _, kwargs = mock_send_mail.call_args
        self.assertIn('Draft PO #99', kwargs['message'])

    @override_settings(REORDER_ALERT_RECIPIENTS=[])
    def test_no_email_sent_when_no_recipients_configured(self):
        part = _mock_part(pk=1, on_hand=2, reorder_point=5, needs_reorder=0)
        output, _, _, mock_send_mail = self._run([part])

        mock_send_mail.assert_not_called()
        self.assertIn('no email sent', output)

    def test_no_parts_with_reorder_point_is_a_no_op(self):
        output, _, mock_draft, mock_send_mail = self._run([])

        self.assertIn('Scanned 0 part(s)', output)
        mock_draft.assert_not_called()
        mock_send_mail.assert_not_called()
