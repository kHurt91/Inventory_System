from django.test import SimpleTestCase
from django.urls import Resolver404, resolve

from apps.inventory.views import (
    EquipmentListViewSet,
    InventoryTransactionViewSet,
    PartsViewSet,
    PurchaseOrderLineViewSet,
    PurchaseOrderViewSet,
    RepairHistoryViewSet,
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

    def test_repair_history_list_resolves_to_viewset(self):
        match = resolve('/api/repair-history/')
        self.assertIs(match.func.cls, RepairHistoryViewSet)

    def test_purchase_orders_list_resolves_to_viewset(self):
        match = resolve('/api/purchase-orders/')
        self.assertIs(match.func.cls, PurchaseOrderViewSet)

    def test_purchase_order_lines_list_resolves_to_viewset(self):
        match = resolve('/api/purchase-order-lines/')
        self.assertIs(match.func.cls, PurchaseOrderLineViewSet)

    def test_purchase_order_submit_action_resolves(self):
        match = resolve('/api/purchase-orders/1/submit/')
        self.assertIs(match.func.cls, PurchaseOrderViewSet)

    def test_purchase_order_receive_action_resolves(self):
        match = resolve('/api/purchase-orders/1/receive/')
        self.assertIs(match.func.cls, PurchaseOrderViewSet)

    def test_parts_lookup_action_resolves(self):
        match = resolve('/api/parts/lookup/')
        self.assertIs(match.func.cls, PartsViewSet)
