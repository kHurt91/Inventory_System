from django.contrib import admin
from apps.inventory.models import models

# Register your models here.

from django.contrib import admin
from . import models


# ---- reusable read-only base for pipeline/history tables ----
class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(models.EquipmentList)
class EquipmentListAdmin(admin.ModelAdmin):
    list_display = ("equipment_id", "make", "model", "year", "status", "owned_by")
    list_filter = ("status", "asset_category", "owned_by")
    search_fields = ("equipment_id", "make", "model", "serial_number")


@admin.register(models.Parts)
class PartsAdmin(admin.ModelAdmin):
    list_display = ("part_id", "part_description", "manufacturer", "on_hand", "needs_reorder", "status")
    list_filter = ("status", "needs_reorder", "manufacturer")
    search_fields = ("part_name", "part_description", "brand_model, manufacturer")
    autocomplete_fields = ("supplier",)          # FK dropdown -> searchable


@admin.register(models.Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    list_display = ("supplier_name", "supplier_type", "phone_number", "email", "status")
    list_filter = ("supplier_type", "status")
    search_fields = ("supplier_name", "email", "phone_number")   # needed for autocomplete above


@admin.register(models.RepairHistory)
class RepairHistoryAdmin(admin.ModelAdmin):
    list_display = ("work_order_number", "equipment", "part", "date_issued", "completed_by", "date_completed")
    list_filter = ("date_issued", "completed_by")
    search_fields = ("work_order_number", "svc_description", "asset_id")
    autocomplete_fields = ("equipment", "part")
    date_hierarchy = "date_issued"


@admin.register(models.PurchaseOrderHistory)
class PurchaseOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ("po_number", "part", "supplier", "date_issued", "actual_cost", "equipment")
    search_fields = ("po_number", "part_description", "supplier")
    autocomplete_fields = ("part", "equipment")
    date_hierarchy = "date_issued"


@admin.register(models.InventoryTransactions)
class InventoryTransactionsAdmin(admin.ModelAdmin):
    list_display = ("part_id","part_description","transaction_type", "quantity", "signed_quantity", "created_time")
    list_filter = ("transaction_type",)
    autocomplete_fields = ("part",)

    @admin.display(description="part_id", ordering="part__part_id")
    def part_name(self, obj):
        return obj.part.part_id if obj.part else "-"
    
    @admin.display(description="part_description", ordering="part__part_description")
    def part_description(self, obj):
        return obj.part.part_description if obj.part else "-"


# ---- history/log tables: visible but read-only ----
admin.site.register(models.SageHistory, ReadOnlyAdmin)
admin.site.register(models.SuppliersLogs, ReadOnlyAdmin)

# ---- simple registrations for the rest ----
admin.site.register(models.OfficeAndCleaningSupplies)
admin.site.register(models.OfficeSupplyTransactions)
admin.site.register(models.PartsDiagrams)
admin.site.register(models.BuildSheets)
admin.site.register(models.AssetEquipmentMapping)
