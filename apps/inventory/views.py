from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .models import EquipmentList, InventoryTransactions, Parts, Suppliers
from .permissions import IsStaffOrReadOnly
from .serializers import (
    EquipmentListSerializer,
    InventoryTransactionSerializer,
    PartsSerializer,
    SupplierSerializer,
)


class PartsViewSet(viewsets.ModelViewSet):
    queryset = Parts.objects.all().order_by('part_id')
    serializer_class = PartsSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['status', 'needs_reorder', 'manufacturer', 'supplier']
    search_fields = ['part_name', 'part_description', 'brand_model', 'manufacturer']
    ordering_fields = ['part_id', 'on_hand', 'part_name']

    
    @action(detail=False, methods=["get"])
    def part_name(self, request):
        part_name = request.query_params.get("part_name")
        if part_name:
            parts = Parts.objects.filter(part_name=part_name)
            if not len(parts) > 0:
                return Response([], status=status.HTTP_200_OK)
            info = PartsSerializer(parts)
            return (info.data)
        

class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransactions.objects.all().order_by('-created_time')
    serializer_class = InventoryTransactionSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['transaction_type', 'part']
    search_fields = ['transaction_type']
    ordering_fields = ['created_time', 'quantity']


class EquipmentListViewSet(viewsets.ModelViewSet):
    queryset = EquipmentList.objects.all().order_by('equipment_id')
    serializer_class = EquipmentListSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['status', 'asset_category', 'owned_by']
    search_fields = ['equipment_id', 'make', 'model', 'serial_number']
    ordering_fields = ['equipment_id', 'year']


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Suppliers.objects.all().order_by('supplier_name')
    serializer_class = SupplierSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['supplier_type', 'status']
    search_fields = ['supplier_name', 'email', 'phone_number']
    ordering_fields = ['supplier_name']
