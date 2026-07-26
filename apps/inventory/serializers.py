from rest_framework import serializers

from .models import EquipmentList, InventoryTransactions, Parts, Suppliers
from .services import InsufficientStockError, record_transaction


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'


class EquipmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentList
        fields = '__all__'


class PartsSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Parts
        fields = [
            'part_id', 'part_description', 'in_stock_location', 'on_hand',
            'equipment_fitment', 'record_id', 'needs_reorder', 'manufacturer',
            'supplier', 'supplier_name', 'alternate_supplier', 'cost_notes',
            'brand_model', 'part_name', 'status',
        ]

    def get_supplier_name(self, obj):
        return obj.supplier.supplier_name if obj.supplier_id else None


class InventoryTransactionSerializer(serializers.ModelSerializer):
    part_description = serializers.SerializerMethodField(read_only=True)
    transaction_type = serializers.ChoiceField(choices=InventoryTransactions.TransactionType.choices)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by_username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InventoryTransactions
        fields = [
            'id', 'part', 'part_description', 'transaction_type',
            'quantity', 'signed_quantity', 'created_time',
            'created_by', 'created_by_username', 'source_reference',
        ]
        read_only_fields = ['signed_quantity', 'created_time']

    def get_part_description(self, obj):
        return obj.part.part_description if obj.part_id else None

    def get_created_by_username(self, obj):
        return obj.created_by.username if obj.created_by_id else None

    def create(self, validated_data):
        validated_data.pop('signed_quantity', None)
        try:
            return record_transaction(
                part=validated_data.get('part'),
                transaction_type=validated_data['transaction_type'],
                quantity=validated_data.get('quantity'),
                created_by=validated_data.pop('created_by', None),
                source_reference=validated_data.get('source_reference'),
            )
        except InsufficientStockError as exc:
            raise serializers.ValidationError({'quantity': str(exc)}) from exc
