from django.test import SimpleTestCase
from django.urls import Resolver404, resolve

from apps.inventory.views import (
    EquipmentListViewSet,
    InventoryTransactionViewSet,
    PartsViewSet,
    SupplierViewSet,
)


class UrlResolutionTests(SimpleTestCase):
    def test_admin_resolves(self):
        try:
            resolve('/admin/')
        except Resolver404:
            self.fail('/admin/ did not resolve')

    def test_token_endpoints_resolve(self):
        self.assertEqual(resolve('/api/token/').url_name, 'token_obtain_pair')
        self.assertEqual(resolve('/api/token/refresh/').url_name, 'token_refresh')

    def test_parts_list_resolves_to_viewset(self):
        match = resolve('/api/parts/')
        self.assertIs(match.func.cls, PartsViewSet)

    def test_inventory_transactions_list_resolves_to_viewset(self):
        match = resolve('/api/inventory-transactions/')
        self.assertIs(match.func.cls, InventoryTransactionViewSet)

    def test_equipment_list_resolves_to_viewset(self):
        match = resolve('/api/equipment/')
        self.assertIs(match.func.cls, EquipmentListViewSet)

    def test_suppliers_list_resolves_to_viewset(self):
        match = resolve('/api/suppliers/')
        self.assertIs(match.func.cls, SupplierViewSet)
