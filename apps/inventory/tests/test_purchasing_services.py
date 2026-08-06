from unittest import mock
from unittest.mock import Mock

from django.test import TestCase

from apps.inventory.models import InventoryTransactions, PurchaseOrder
from apps.inventory.purchasing_services import (
    InvalidPurchaseOrderStateError,
    draft_purchase_orders_from_reorder_alerts,
    receive_purchase_order_line,
    submit_purchase_order,
)

Status = PurchaseOrder.Status
TT = InventoryTransactions.TransactionType


def _mock_part(pk, supplier_id, reorder_quantity=None, part_description='Widget'):
    return Mock(pk=pk, supplier_id=supplier_id, reorder_quantity=reorder_quantity, part_description=part_description)


class DraftPurchaseOrdersFromReorderAlertsTests(TestCase):
    def _patched(self):
        return mock.patch.multiple(
            'apps.inventory.purchasing_services',
            PurchaseOrder=mock.DEFAULT,
            PurchaseOrderLine=mock.DEFAULT,
            PartsSuppliers=mock.DEFAULT,
        )

    def test_groups_parts_by_supplier_into_one_po_each(self):
        part_a = _mock_part(pk=1, supplier_id=100)
        part_b = _mock_part(pk=2, supplier_id=100)
        part_c = _mock_part(pk=3, supplier_id=200)

        with self._patched() as mocks:
            mocks['PartsSuppliers'].objects.filter.return_value.values_list.return_value.first.return_value = None
            po_for_100 = Mock()
            po_for_200 = Mock()
            mocks['PurchaseOrder'].objects.create.side_effect = [po_for_100, po_for_200]
            mocks['PurchaseOrder'].Status = Status

            result = draft_purchase_orders_from_reorder_alerts([part_a, part_b, part_c])

            self.assertEqual(result, [po_for_100, po_for_200])
            self.assertEqual(mocks['PurchaseOrder'].objects.create.call_count, 2)
            # 2 lines for supplier 100's PO, 1 line for supplier 200's PO
            self.assertEqual(mocks['PurchaseOrderLine'].objects.create.call_count, 3)

    def test_parts_without_supplier_are_skipped(self):
        part = _mock_part(pk=1, supplier_id=None)

        with self._patched() as mocks:
            result = draft_purchase_orders_from_reorder_alerts([part])

            self.assertEqual(result, [])
            mocks['PurchaseOrder'].objects.create.assert_not_called()
            mocks['PurchaseOrderLine'].objects.create.assert_not_called()

    def test_empty_parts_iterable_returns_no_orders(self):
        with self._patched() as mocks:
            result = draft_purchase_orders_from_reorder_alerts([])

            self.assertEqual(result, [])
            mocks['PurchaseOrder'].objects.create.assert_not_called()

    def test_line_quantity_defaults_to_one_when_reorder_quantity_unset(self):
        part = _mock_part(pk=1, supplier_id=100, reorder_quantity=None)

        with self._patched() as mocks:
            mocks['PartsSuppliers'].objects.filter.return_value.values_list.return_value.first.return_value = None
            mocks['PurchaseOrder'].objects.create.return_value = Mock()

            draft_purchase_orders_from_reorder_alerts([part])

            _, kwargs = mocks['PurchaseOrderLine'].objects.create.call_args
            self.assertEqual(kwargs['quantity_ordered'], 1)

    def test_price_is_snapshotted_from_parts_suppliers(self):
        part = _mock_part(pk=1, supplier_id=100, reorder_quantity=5)

        with self._patched() as mocks:
            mocks['PartsSuppliers'].objects.filter.return_value.values_list.return_value.first.return_value = '19.99'
            mocks['PurchaseOrder'].objects.create.return_value = Mock()

            draft_purchase_orders_from_reorder_alerts([part])

            _, kwargs = mocks['PurchaseOrderLine'].objects.create.call_args
            self.assertEqual(kwargs['unit_price'], '19.99')
            self.assertEqual(kwargs['quantity_ordered'], 5)


class SubmitPurchaseOrderTests(TestCase):
    def _mock_po(self, status, has_lines=True):
        return Mock(status=status, lines=Mock(exists=Mock(return_value=has_lines)))

    def test_submits_draft_with_lines(self):
        po = self._mock_po(Status.DRAFT, has_lines=True)

        result = submit_purchase_order(po)

        self.assertIs(result, po)
        self.assertEqual(po.status, Status.SUBMITTED)
        self.assertIsNotNone(po.submitted_at)
        po.save.assert_called_once_with(update_fields=['status', 'submitted_at'])

    def test_raises_if_not_draft(self):
        po = self._mock_po(Status.SUBMITTED)

        with self.assertRaises(InvalidPurchaseOrderStateError):
            submit_purchase_order(po)

        po.save.assert_not_called()

    def test_raises_if_no_lines(self):
        po = self._mock_po(Status.DRAFT, has_lines=False)

        with self.assertRaises(InvalidPurchaseOrderStateError):
            submit_purchase_order(po)

        po.save.assert_not_called()


class ReceivePurchaseOrderLineTests(TestCase):
    def _mock_line(self, po, quantity_ordered, quantity_received=0, part=None):
        return Mock(
            purchase_order=po, part=part or Mock(), quantity_ordered=quantity_ordered,
            quantity_received=quantity_received, pk=1,
        )

    def test_receiving_full_quantity_marks_po_received(self):
        po = Mock(status=Status.SUBMITTED, pk=10)
        line = self._mock_line(po, quantity_ordered=5, quantity_received=0)
        po.lines.all.return_value = [line]

        with mock.patch('apps.inventory.purchasing_services.record_transaction') as mock_record:
            receive_purchase_order_line(line=line, quantity=5, created_by=None)

            mock_record.assert_called_once_with(
                part=line.part, transaction_type=TT.RECEIVE_FROM_SUPPLIER,
                quantity=5, created_by=None, source_reference='PO-10',
            )
            self.assertEqual(line.quantity_received, 5)
            line.save.assert_called_once_with(update_fields=['quantity_received'])
            self.assertEqual(po.status, Status.RECEIVED)
            self.assertIsNotNone(po.received_at)
            po.save.assert_called_once_with(update_fields=['status', 'received_at'])

    def test_receiving_partial_quantity_keeps_po_submitted(self):
        po = Mock(status=Status.SUBMITTED, pk=10)
        line = self._mock_line(po, quantity_ordered=5, quantity_received=0)
        po.lines.all.return_value = [line]

        with mock.patch('apps.inventory.purchasing_services.record_transaction'):
            receive_purchase_order_line(line=line, quantity=2, created_by=None)

            self.assertEqual(line.quantity_received, 2)
            po.save.assert_not_called()

    def test_raises_if_po_not_submitted(self):
        po = Mock(status=Status.DRAFT, pk=10)
        line = self._mock_line(po, quantity_ordered=5)

        with mock.patch('apps.inventory.purchasing_services.record_transaction') as mock_record:
            with self.assertRaises(InvalidPurchaseOrderStateError):
                receive_purchase_order_line(line=line, quantity=1, created_by=None)
            mock_record.assert_not_called()

    def test_raises_on_non_positive_quantity(self):
        po = Mock(status=Status.SUBMITTED, pk=10)
        line = self._mock_line(po, quantity_ordered=5)

        with self.assertRaises(ValueError):
            receive_purchase_order_line(line=line, quantity=0, created_by=None)

    def test_po_stays_submitted_when_other_lines_still_incomplete(self):
        po = Mock(status=Status.SUBMITTED, pk=10)
        line1 = self._mock_line(po, quantity_ordered=5, quantity_received=0)
        line2 = self._mock_line(po, quantity_ordered=3, quantity_received=1)
        po.lines.all.return_value = [line1, line2]

        with mock.patch('apps.inventory.purchasing_services.record_transaction'):
            receive_purchase_order_line(line=line1, quantity=5, created_by=None)

            self.assertEqual(line1.quantity_received, 5)
            self.assertEqual(po.status, Status.SUBMITTED)
            po.save.assert_not_called()

    def test_raises_on_over_receive(self):
        po = Mock(status=Status.SUBMITTED, pk=10)
        line = self._mock_line(po, quantity_ordered=5, quantity_received=3)

        with mock.patch('apps.inventory.purchasing_services.record_transaction') as mock_record:
            with self.assertRaises(ValueError):
                receive_purchase_order_line(line=line, quantity=5, created_by=None)
            mock_record.assert_not_called()
