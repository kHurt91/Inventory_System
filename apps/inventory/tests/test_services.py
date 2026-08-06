from unittest import mock
from unittest.mock import Mock

from django.test import TestCase

from apps.inventory.models import InventoryTransactions
from apps.inventory.services import (
    InsufficientStockError,
    compute_signed_quantity,
    record_transaction,
)

TT = InventoryTransactions.TransactionType


class ComputeSignedQuantityTests(TestCase):
    def test_receive_is_positive(self):
        self.assertEqual(compute_signed_quantity(TT.RECEIVE_FROM_SUPPLIER, 5), 5)

    def test_issue_is_negative(self):
        self.assertEqual(compute_signed_quantity(TT.ISSUE, 5), -5)

    def test_return_to_supplier_is_negative(self):
        self.assertEqual(compute_signed_quantity(TT.RETURN_TO_SUPPLIER, 5), -5)

    def test_return_is_positive(self):
        self.assertEqual(compute_signed_quantity(TT.RETURN, 5), 5)

    def test_none_quantity_yields_none(self):
        self.assertIsNone(compute_signed_quantity(TT.ISSUE, None))

    def test_unknown_transaction_type_yields_none(self):
        self.assertIsNone(compute_signed_quantity('BOGUS', 5))


class RecordTransactionTests(TestCase):
    def _mock_part(self, on_hand, reorder_point=None):
        return Mock(pk=1, on_hand=on_hand, reorder_point=reorder_point)

    def test_issue_decrements_on_hand_and_creates_transaction(self):
        part = self._mock_part(on_hand=10)
        with mock.patch('apps.inventory.services.Parts') as MockParts, \
                mock.patch('apps.inventory.services.InventoryTransactions') as MockTxn:
            MockParts.objects.select_for_update.return_value.get.return_value = part

            record_transaction(part=part, transaction_type=TT.ISSUE, quantity=3, created_by=None)

            MockParts.objects.select_for_update.return_value.get.assert_called_once_with(pk=1)
            MockParts.objects.filter.assert_called_once_with(pk=1)
            MockParts.objects.filter.return_value.update.assert_called_once()
            MockTxn.objects.create.assert_called_once_with(
                part=part, transaction_type=TT.ISSUE, quantity=3,
                signed_quantity=-3, created_by=None, source_reference=None,
            )

    def test_insufficient_stock_raises_and_does_not_write(self):
        part = self._mock_part(on_hand=2)
        with mock.patch('apps.inventory.services.Parts') as MockParts, \
                mock.patch('apps.inventory.services.InventoryTransactions') as MockTxn:
            MockParts.objects.select_for_update.return_value.get.return_value = part

            with self.assertRaises(InsufficientStockError):
                record_transaction(part=part, transaction_type=TT.ISSUE, quantity=5, created_by=None)

            MockParts.objects.filter.return_value.update.assert_not_called()
            MockTxn.objects.create.assert_not_called()

    def test_null_part_is_a_no_op_on_stock(self):
        with mock.patch('apps.inventory.services.Parts') as MockParts, \
                mock.patch('apps.inventory.services.InventoryTransactions') as MockTxn:
            record_transaction(
                part=None, transaction_type=TT.RECEIVE_FROM_SUPPLIER, quantity=5, created_by=None
            )
            MockParts.objects.select_for_update.assert_not_called()
            MockTxn.objects.create.assert_called_once()

    def test_needs_reorder_set_when_on_hand_falls_to_or_below_reorder_point(self):
        part = self._mock_part(on_hand=10, reorder_point=5)
        with mock.patch('apps.inventory.services.Parts') as MockParts, \
                mock.patch('apps.inventory.services.InventoryTransactions'):
            MockParts.objects.select_for_update.return_value.get.return_value = part

            record_transaction(part=part, transaction_type=TT.ISSUE, quantity=5, created_by=None)

            _, kwargs = MockParts.objects.filter.return_value.update.call_args
            self.assertEqual(kwargs['needs_reorder'], 1)

    def test_needs_reorder_cleared_when_on_hand_stays_above_reorder_point(self):
        part = self._mock_part(on_hand=10, reorder_point=5)
        with mock.patch('apps.inventory.services.Parts') as MockParts, \
                mock.patch('apps.inventory.services.InventoryTransactions'):
            MockParts.objects.select_for_update.return_value.get.return_value = part

            record_transaction(part=part, transaction_type=TT.ISSUE, quantity=1, created_by=None)

            _, kwargs = MockParts.objects.filter.return_value.update.call_args
            self.assertEqual(kwargs['needs_reorder'], 0)

    def test_needs_reorder_omitted_when_reorder_point_unset(self):
        part = self._mock_part(on_hand=10, reorder_point=None)
        with mock.patch('apps.inventory.services.Parts') as MockParts, \
                mock.patch('apps.inventory.services.InventoryTransactions'):
            MockParts.objects.select_for_update.return_value.get.return_value = part

            record_transaction(part=part, transaction_type=TT.ISSUE, quantity=1, created_by=None)

            _, kwargs = MockParts.objects.filter.return_value.update.call_args
            self.assertNotIn('needs_reorder', kwargs)

    def test_empty_source_reference_is_stored_as_none(self):
        part = self._mock_part(on_hand=10)
        with mock.patch('apps.inventory.services.Parts') as MockParts, \
                mock.patch('apps.inventory.services.InventoryTransactions') as MockTxn:
            MockParts.objects.select_for_update.return_value.get.return_value = part

            record_transaction(
                part=part, transaction_type=TT.ISSUE, quantity=1,
                created_by=None, source_reference='',
            )

            _, kwargs = MockTxn.objects.create.call_args
            self.assertIsNone(kwargs['source_reference'])

    def test_unrecognized_transaction_type_skips_stock_update(self):
        part = self._mock_part(on_hand=10)
        with mock.patch('apps.inventory.services.Parts') as MockParts, \
                mock.patch('apps.inventory.services.InventoryTransactions') as MockTxn:
            record_transaction(part=part, transaction_type='BOGUS', quantity=5, created_by=None)

            MockParts.objects.select_for_update.assert_not_called()
            MockParts.objects.filter.return_value.update.assert_not_called()
            MockTxn.objects.create.assert_called_once_with(
                part=part, transaction_type='BOGUS', quantity=5,
                signed_quantity=None, created_by=None, source_reference=None,
            )
