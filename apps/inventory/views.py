from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    EquipmentList,
    InventoryTransactions,
    Parts,
    PurchaseOrder,
    PurchaseOrderLine,
    RepairHistory,
    Suppliers,
)
from .permissions import IsStaffOrReadOnly
from .purchasing_services import InvalidPurchaseOrderStateError, receive_purchase_order_line, submit_purchase_order
from .serializers import (
    EquipmentListSerializer,
    InventoryTransactionSerializer,
    PartsSerializer,
    PurchaseOrderLineSerializer,
    PurchaseOrderSerializer,
    RepairHistorySerializer,
    SupplierSerializer,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def whoami(request):
    return Response({
        'username': request.user.username,
        'is_staff': request.user.is_staff,
    })


class PartsViewSet(viewsets.ModelViewSet):
    queryset = Parts.objects.all().order_by('part_id')
    serializer_class = PartsSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = [
        'status', 'needs_reorder', 'reorder_point', 'reorder_quantity', 'manufacturer', 'supplier', 'barcode',
    ]
    search_fields = ['part_name', 'part_description', 'brand_model', 'manufacturer', 'barcode']
    ordering_fields = ['part_id', 'on_hand', 'part_name']


    @action(detail=False, methods=["get"])
    def part_name(self, request):
        part_name = request.query_params.get("part_name")
        if part_name:
            parts = Parts.objects.filter(part_name=part_name)
            if not len(parts) > 0:
                return Response([], status=status.HTTP_200_OK)
            info = PartsSerializer(parts, many=True)
            return Response(info.data)
        return Response([], status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def lookup(self, request):
        """
        Barcode/QR scan lookup for the mobile client. Matches against `barcode`
        first (the intended long-term identifier once parts are physically
        re-labeled), then falls back to part_id/part_name so scanning still
        works for parts that haven't been barcoded yet.
        """
        code = request.query_params.get('code')
        if not code:
            return Response({'detail': 'code query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        part = Parts.objects.filter(barcode=code).first()
        if part is None and code.isdigit():
            part = Parts.objects.filter(part_id=int(code)).first()
        if part is None:
            part = Parts.objects.filter(part_name=code).first()

        if part is None:
            return Response({'detail': 'No part matches that code.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(part).data)


class InventoryTransactionViewSet(viewsets.ModelViewSet):
    queryset = InventoryTransactions.objects.all().order_by('-created_time')
    serializer_class = InventoryTransactionSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['transaction_type', 'part']
    search_fields = ['transaction_type']
    ordering_fields = ['created_time', 'quantity']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


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


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().order_by('-created_at')
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['status', 'supplier', 'auto_generated']
    search_fields = ['notes']
    ordering_fields = ['created_at', 'submitted_at', 'received_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        purchase_order = self.get_object()
        try:
            submit_purchase_order(purchase_order)
        except InvalidPurchaseOrderStateError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(purchase_order).data)

    @action(detail=True, methods=['post'])
    def receive(self, request, pk=None):
        purchase_order = self.get_object()
        line_id = request.data.get('line')
        quantity = request.data.get('quantity')
        if line_id is None or quantity is None:
            return Response({'detail': 'line and quantity are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            line = purchase_order.lines.get(pk=line_id)
        except PurchaseOrderLine.DoesNotExist:
            return Response({'detail': 'Line not found on this purchase order.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            receive_purchase_order_line(line=line, quantity=int(quantity), created_by=request.user)
        except (InvalidPurchaseOrderStateError, ValueError) as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(purchase_order).data)


class PurchaseOrderLineViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderLine.objects.all().order_by('id')
    serializer_class = PurchaseOrderLineSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['purchase_order', 'part']
    ordering_fields = ['id']

    def perform_create(self, serializer):
        purchase_order = serializer.validated_data['purchase_order']
        if purchase_order.status != PurchaseOrder.Status.DRAFT:
            raise ValidationError('Cannot add line items to a purchase order that is not in Draft status.')
        serializer.save()


class RepairHistoryViewSet(viewsets.ModelViewSet):
    queryset = RepairHistory.objects.all().order_by('-date_issued')
    serializer_class = RepairHistorySerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ['completed_by','equipment', 'part', 'date_completed']
    search_fields = ['work_order_number', 'svc_description', 'mechanic_notes', 'reported_by', 'asset_id']
    ordering_fields = ['date_issued', 'date_needed', 'date_completed', 'hours_to_complete']
