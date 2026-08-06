from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    EquipmentListViewSet,
    InventoryTransactionViewSet,
    PartsViewSet,
    PurchaseOrderLineViewSet,
    PurchaseOrderViewSet,
    SupplierViewSet,
    RepairHistoryViewSet,
    whoami,
)

router = DefaultRouter()
router.register(r'parts', PartsViewSet, basename='parts')
router.register(r'inventory-transactions', InventoryTransactionViewSet, basename='inventory-transactions')
router.register(r'equipment', EquipmentListViewSet, basename='equipment')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'repair-history', RepairHistoryViewSet, basename='repair-history')
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-orders')
router.register(r'purchase-order-lines', PurchaseOrderLineViewSet, basename='purchase-order-lines')

urlpatterns = [
    path('me/', whoami, name='whoami'),
] + router.urls
