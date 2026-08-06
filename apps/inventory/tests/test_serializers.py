from unittest import mock

from django.test import SimpleTestCase
from rest_framework import serializers as drf_serializers

from apps.inventory.serializers import (
    EquipmentListSerializer,
    InventoryTransactionSerializer,
    PartsSerializer,
    PurchaseOrderLineSerializer,
    PurchaseOrderSerializer,
    RepairHistorySerializer,
    SupplierSerializer,
)
from apps.inventory.services import InsufficientStockError


class PartsSerializerTests(SimpleTestCase):
    def test_valid_without_fk(self):
        serializer = PartsSerializer(data={'part_description': 'Test Part', 'on_hand': 5})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_needs_reorder_is_read_only(self):
        # needs_reorder is derived by record_transaction()/scan_reorder_alerts,
        # so client-supplied values (even invalid ones) are silently ignored.
        serializer = PartsSerializer(data={'part_description': 'Test Part', 'needs_reorder': 'not-an-int'})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('needs_reorder', serializer.validated_data)

    def test_barcode_is_optional_and_writable(self):
        serializer = PartsSerializer(data={'part_description': 'Test Part', 'barcode': 'SCAN-001'})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['barcode'], 'SCAN-001')


class InventoryTransactionSerializerTests(SimpleTestCase):
    def test_valid_without_fk(self):
        serializer = InventoryTransactionSerializer(data={
            'transaction_type': 'Issue',
            'quantity': 3,
            'signed_quantity': -3,
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_quantity_type(self):
        serializer = InventoryTransactionSerializer(data={
            'transaction_type': 'Issue',
            'quantity': 'not-a-number',
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_invalid_transaction_type_is_rejected(self):
        serializer = InventoryTransactionSerializer(data={'transaction_type': 'Bogus', 'quantity': 1})
        self.assertFalse(serializer.is_valid())
        self.assertIn('transaction_type', serializer.errors)

    def test_client_supplied_signed_quantity_is_read_only(self):
        serializer = InventoryTransactionSerializer(
            data={'transaction_type': 'Issue', 'quantity': 3, 'signed_quantity': 999}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('signed_quantity', serializer.validated_data)

    def test_client_supplied_created_by_is_read_only(self):
        serializer = InventoryTransactionSerializer(
            data={'transaction_type': 'Issue', 'quantity': 3, 'created_by': 999}
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('created_by', serializer.validated_data)


class InventoryTransactionSerializerCreateTests(SimpleTestCase):
    def test_create_delegates_to_record_transaction_and_strips_signed_quantity(self):
        with mock.patch('apps.inventory.serializers.record_transaction') as mock_record:
            serializer = InventoryTransactionSerializer(data={
                'transaction_type': 'Issue', 'quantity': 3, 'signed_quantity': 999,
            })
            self.assertTrue(serializer.is_valid(), serializer.errors)
            serializer.save()

            self.assertEqual(mock_record.call_count, 1)
            _, kwargs = mock_record.call_args
            self.assertNotIn('signed_quantity', kwargs)
            self.assertEqual(kwargs['transaction_type'], 'Issue')
            self.assertEqual(kwargs['quantity'], 3)

    def test_create_converts_insufficient_stock_error_to_validation_error(self):
        with mock.patch(
            'apps.inventory.serializers.record_transaction',
            side_effect=InsufficientStockError('not enough stock'),
        ):
            serializer = InventoryTransactionSerializer(data={'transaction_type': 'Issue', 'quantity': 3})
            self.assertTrue(serializer.is_valid(), serializer.errors)
            with self.assertRaises(drf_serializers.ValidationError) as ctx:
                serializer.save()
            self.assertIn('quantity', ctx.exception.detail)


class EquipmentListSerializerTests(SimpleTestCase):
    def test_valid_minimal(self):
        serializer = EquipmentListSerializer(data={'make': 'Ford', 'model': 'F350', 'year': 2020})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_year_type(self):
        serializer = EquipmentListSerializer(data={'year': 'not-a-year'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('year', serializer.errors)


class SupplierSerializerTests(SimpleTestCase):
    def test_valid_minimal(self):
        serializer = SupplierSerializer(data={'supplier_name': 'Acme Parts'})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_last_purchase_date_type(self):
        serializer = SupplierSerializer(data={'last_purchase_date': 'not-a-date'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('last_purchase_date', serializer.errors)


class PurchaseOrderSerializerTests(SimpleTestCase):
    def test_missing_supplier_is_invalid(self):
        serializer = PurchaseOrderSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('supplier', serializer.errors)

    def test_status_is_read_only(self):
        # status only changes via the submit/receive service actions, so a client-supplied
        # value is silently ignored rather than validated against the choices.
        serializer = PurchaseOrderSerializer(data={'status': 'not-a-real-status'})
        self.assertFalse(serializer.is_valid())
        self.assertNotIn('status', serializer.errors)
        self.assertIn('supplier', serializer.errors)


class PurchaseOrderLineSerializerTests(SimpleTestCase):
    def test_missing_required_fields_is_invalid(self):
        serializer = PurchaseOrderLineSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('purchase_order', serializer.errors)
        self.assertIn('part', serializer.errors)
        self.assertIn('quantity_ordered', serializer.errors)

    def test_quantity_received_is_read_only(self):
        serializer = PurchaseOrderLineSerializer(data={'quantity_received': 'not-an-int'})
        self.assertFalse(serializer.is_valid())
        self.assertNotIn('quantity_received', serializer.errors)


class RepairHistorySerializerTests(SimpleTestCase):
    def test_valid_without_fk(self):
        serializer = RepairHistorySerializer(data={'work_order_number': 'WO-1', 'svc_description': 'Test'})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_hours_to_complete_type(self):
        serializer = RepairHistorySerializer(data={'hours_to_complete': 'not-a-number'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('hours_to_complete', serializer.errors)
