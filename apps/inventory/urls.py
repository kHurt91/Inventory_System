from rest_framework.routers import DefaultRouter

from .views import (
    EquipmentListViewSet,
    InventoryTransactionViewSet,
    PartsViewSet,
    SupplierViewSet,
)

router = DefaultRouter()
router.register(r'parts', PartsViewSet, basename='parts')
router.register(r'inventory-transactions', InventoryTransactionViewSet, basename='inventory-transactions')
router.register(r'equipment', EquipmentListViewSet, basename='equipment')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')

urlpatterns = router.urls
