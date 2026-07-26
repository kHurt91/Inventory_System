from django.test import SimpleTestCase

from apps.inventory.serializers import (
    EquipmentListSerializer,
    InventoryTransactionSerializer,
    PartsSerializer,
    SupplierSerializer,
)


class PartsSerializerTests(SimpleTestCase):
    def test_valid_without_fk(self):
        serializer = PartsSerializer(data={'part_description': 'Test Part', 'on_hand': 5})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_needs_reorder_type(self):
        serializer = PartsSerializer(data={'needs_reorder': 'not-an-int'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('needs_reorder', serializer.errors)


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
