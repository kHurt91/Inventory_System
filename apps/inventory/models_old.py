# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AssetEquipmentMapping(models.Model):
    last_updated = models.TextField(db_column='Last Updated', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    asset_id = models.ForeignKey('EquipmentList', models.DO_NOTHING, db_column='Asset ID', to_field='Asset ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_id = models.TextField(db_column='Equipment ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    active_field = models.IntegerField(db_column='Active?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    airtable_id = models.TextField(blank=True, null=True)
    equipment_list_2 = models.TextField(db_column='Equipment List 2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'asset_equipment_mapping'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BuildSheets(models.Model):
    pk = models.CompositePrimaryKey('id', 'Equipment ID')
    id = models.AutoField()
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    build_sheet = models.TextField(db_column='Build Sheet', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_id = models.ForeignKey('EquipmentList', models.DO_NOTHING, db_column='Equipment ID', to_field='Build Sheet')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'build_sheets'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EquipmentList(models.Model):
    record_id = models.TextField(db_column='Record ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    make = models.TextField(db_column='Make', blank=True, null=True)  # Field name made lowercase.
    model = models.TextField(db_column='Model', blank=True, null=True)  # Field name made lowercase.
    owned_by = models.TextField(db_column='Owned By', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year = models.FloatField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    asset_category = models.TextField(db_column='Asset Category', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_id = models.TextField(db_column='Equipment ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    serial_number = models.TextField(db_column='Serial Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_notes = models.TextField(db_column='Equipment Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    part_compatibility = models.TextField(db_column='Part Compatibility', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tires = models.TextField(db_column='Tires', blank=True, null=True)  # Field name made lowercase.
    manuals = models.TextField(db_column='Manuals', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    serial_number_field = models.TextField(db_column='Serial Number!', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    equipment_name = models.TextField(db_column='Equipment Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    update_equipment_requests = models.TextField(db_column='Update Equipment Requests', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    asset_id_from_asset_equipment_mapping_field = models.TextField(db_column='Asset ID (from Asset ↔ Equipment Mapping)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    repair_history_2 = models.TextField(db_column='Repair History 2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    asset_id_from_equip_dbase_field = models.TextField(db_column='Asset ID (From Equip Dbase)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'equipment list'


class EquipmentList(models.Model):
    record_id = models.TextField(db_column='Record ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    make = models.TextField(db_column='Make', blank=True, null=True)  # Field name made lowercase.
    model = models.TextField(db_column='Model', blank=True, null=True)  # Field name made lowercase.
    owned_by = models.TextField(db_column='Owned By', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    year = models.FloatField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    asset_category = models.TextField(db_column='Asset Category', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_id = models.IntegerField(db_column='Equipment ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    serial_number = models.TextField(db_column='Serial Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_notes = models.TextField(db_column='Equipment Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    part_compatibility = models.TextField(db_column='Part Compatibility', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    tires = models.TextField(db_column='Tires', blank=True, null=True)  # Field name made lowercase.
    manuals = models.TextField(db_column='Manuals', blank=True, null=True)  # Field name made lowercase.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    build_sheet = models.IntegerField(db_column='Build Sheet', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    asset_id = models.IntegerField(db_column='Asset ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    alt_asset_id = models.IntegerField(db_column='ALT Asset ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'equipment_list'

class InventoryTransactions(models.Model):
    id = models.OneToOneField('Parts', models.DO_NOTHING, db_column='id', primary_key=True)
    signed_quantity = models.ForeignKey('Parts', models.DO_NOTHING, db_column='Signed Quantity', to_field='On Hand', related_name='inventorytransactions_signed_quantity_set', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transaction_type = models.TextField(db_column='Transaction Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    created_time = models.TextField(db_column='Created Time', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    quantity = models.BigIntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    airtable_id = models.TextField(blank=True, null=True)
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'inventory_transactions'

class OfficeAndCleaningSupplies(models.Model):
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    minimum_quantity = models.BigIntegerField(db_column='Minimum Quantity', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    category = models.TextField(db_column='Category', blank=True, null=True)  # Field name made lowercase.
    in_stock_location = models.TextField(db_column='In-Stock Location', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    office_supply_transactions = models.TextField(db_column='Office Supply Transactions', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    on_hand = models.BigIntegerField(db_column='On Hand', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    supply_name = models.TextField(db_column='Supply Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    supplier_name = models.TextField(db_column='Supplier Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'office_and_cleaning_supplies'


class OfficeAndCleaningSuppliesHasSuppliersGridView(models.Model):
    pk = models.CompositePrimaryKey('office_and_cleaning_supplies_id', 'suppliers_grid_view_id')
    office_and_cleaning_supplies = models.ForeignKey(OfficeAndCleaningSupplies, models.DO_NOTHING)
    suppliers_grid_view = models.ForeignKey('Suppliers', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'office_and_cleaning_supplies_has_suppliers_grid_view'


class OfficeSupplyTransactions(models.Model):
    supply_name = models.TextField(db_column='Supply Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    transaction_type = models.TextField(db_column='Transaction Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    office_supply = models.ForeignKey(OfficeAndCleaningSupplies, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'office_supply_transactions'


class Parts(models.Model):
    part_description = models.TextField(db_column='Part Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    in_stock_location = models.TextField(db_column='In-Stock Location', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    on_hand = models.BigIntegerField(db_column='On Hand', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_fitment = models.TextField(db_column='Equipment Fitment', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    part_id = models.AutoField(db_column='Part ID', primary_key=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    record_id = models.IntegerField(db_column='Record ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    needs_reorder = models.IntegerField(db_column='Needs Reorder', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    manufacturer = models.TextField(db_column='Manufacturer', blank=True, null=True)  # Field name made lowercase.
    supplier_id = models.IntegerField(db_column='Supplier ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    alternate_supplier = models.TextField(db_column='Alternate Supplier', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    supplier_name = models.TextField(db_column='Supplier Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cost_notes = models.TextField(db_column='Cost Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    brand_model = models.TextField(db_column='Brand / Model', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    part_name = models.TextField(db_column='Part Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    update_part_requests = models.TextField(db_column='Update Part Requests', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    inventory_transactions = models.TextField(db_column='Inventory Transactions', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    repair_history = models.CharField(db_column='Repair History', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sage_history = models.CharField(db_column='Sage History', max_length=255, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    supplier_name_from_supplier_name_field = models.TextField(db_column='Supplier Name (from Supplier Name)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'parts'

class PartsDiagrams(models.Model):
    airtable_id = models.TextField(blank=True, null=True)
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    attachments = models.TextField(db_column='Attachments', blank=True, null=True)  # Field name made lowercase.
    equipment_id = models.ForeignKey(EquipmentList, models.DO_NOTHING, db_column='Equipment ID', to_field='Equipment ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    diagram_description = models.TextField(db_column='Diagram Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    component_part_id = models.IntegerField(db_column='Component_Part ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'parts_diagrams'


class PartsHasEquipmentList(models.Model):
    pk = models.CompositePrimaryKey('parts_Part ID', 'equipment_list_id')
    parts_part_id = models.ForeignKey(Parts, models.DO_NOTHING, db_column='parts_Part ID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_list = models.ForeignKey(EquipmentList, models.DO_NOTHING, to_field='Equipment ID')

    class Meta:
        managed = False
        db_table = 'parts_has_equipment_list'


class PartsSuppliers(models.Model):
    pk = models.CompositePrimaryKey('Part ID', ' Supplier ID')
    id = models.IntegerField()
    part_id = models.ForeignKey(Parts, models.DO_NOTHING, db_column='Part ID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    field_supplier_id = models.ForeignKey('Suppliers', models.DO_NOTHING, db_column=' Supplier ID')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    supplier_part_code = models.TextField(db_column='Supplier Part Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'parts_suppliers'


class PurchaseOrderHistory(models.Model):
    part_description = models.TextField(db_column='Part Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    part_id = models.TextField(db_column='Part ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date_issued = models.TextField(db_column='Date Issued', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    invoice_field = models.DecimalField(db_column='Invoice #', max_digits=22, decimal_places=1, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    po = models.TextField(db_column='PO', blank=True, null=True)  # Field name made lowercase.
    estimated_cost = models.FloatField(db_column='Estimated Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    company = models.TextField(db_column='Company', blank=True, null=True)  # Field name made lowercase.
    supplier = models.TextField(db_column='Supplier', blank=True, null=True)  # Field name made lowercase.
    actual_cost = models.FloatField(db_column='Actual Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    received_date = models.TextField(db_column='Received Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    issued_by = models.TextField(db_column='Issued By', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    shipper_packing_slip_field = models.TextField(db_column='Shipper / Packing Slip #', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    equipment_id = models.ForeignKey(EquipmentList, models.DO_NOTHING, db_column='Equipment ID', to_field='Equipment ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'purchase_order_history'


class PurchaseOrderImportStaging(models.Model):
    mapped_actual_cost = models.FloatField(db_column='Mapped Actual Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    row_number = models.FloatField(db_column='Row Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    mapped_company = models.TextField(db_column='Mapped Company', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    imported_at = models.TextField(db_column='Imported At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_batch_id = models.TextField(db_column='Import Batch ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    raw_json = models.TextField(db_column='Raw JSON', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapping_status = models.TextField(db_column='Mapping Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    error_message = models.TextField(db_column='Error Message', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    attachment_summary = models.TextField(db_column='Attachment Summary', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    source_filename = models.TextField(db_column='Source Filename', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    mapped_equipment_id = models.TextField(db_column='Mapped Equipment ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_notes = models.TextField(db_column='Import Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_issued_by = models.TextField(db_column='Mapped Issued By', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_estimated_cost = models.FloatField(db_column='Mapped Estimated Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_invoice_field = models.FloatField(db_column='Mapped Invoice #', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    promoted_field = models.IntegerField(db_column='Promoted?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    duplicate_field = models.IntegerField(db_column='Duplicate?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    mapped_part_id = models.TextField(db_column='Mapped Part ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_shipper_packing_slip_field = models.TextField(db_column='Mapped Shipper / Packing Slip #', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'purchase_order_import_staging'


class PurchaseOrderUploadIntake(models.Model):
    rows_created = models.BigIntegerField(db_column='Rows Created', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    main_file = models.TextField(db_column='Main File', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parse_status = models.TextField(db_column='Parse Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_batch_id = models.TextField(db_column='Import Batch ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    imported_at = models.TextField(db_column='Imported At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    import_notes = models.TextField(db_column='Import Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'purchase_order_upload_intake'

class RepairImportStaging(models.Model):
    attachment_summary = models.TextField(db_column='Attachment Summary', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    raw_json = models.TextField(db_column='Raw JSON', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_date_issued = models.TextField(db_column='Mapped Date Issued', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    row_number = models.FloatField(db_column='Row Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    error_message = models.TextField(db_column='Error Message', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_batch_id = models.TextField(db_column='Import Batch ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_date_fixed = models.TextField(db_column='Mapped Date Fixed', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_filename = models.TextField(db_column='Source Filename', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    imported_at = models.TextField(db_column='Imported At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapping_status = models.TextField(db_column='Mapping Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_equipment_id = models.TextField(db_column='Mapped Equipment ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_asset_id = models.TextField(db_column='Mapped Asset ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_notes = models.TextField(db_column='Import Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    recheck_mapping_field = models.IntegerField(db_column='Recheck Mapping?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'repair_import_staging'


class RepairUploadIntake(models.Model):
    airtable_id = models.TextField(blank=True, null=True)
    imported_at = models.TextField(db_column='Imported At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_batch_id = models.TextField(db_column='Import Batch ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parse_status = models.TextField(db_column='Parse Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rows_created = models.FloatField(db_column='Rows Created', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    main_file = models.TextField(db_column='Main File', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_notes = models.TextField(db_column='Import Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_filename = models.TextField(db_column='Source Filename', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    core_upload = models.TextField(db_column='Core Upload', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parse_eligible_field = models.IntegerField(db_column='Parse Eligible?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    imported_by_email = models.TextField(db_column='Imported By Email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parse_error = models.TextField(db_column='Parse Error', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'repair_upload_intake'

class RepairHistory(models.Model):
    date_needed = models.TextField(db_column='Date Needed', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date_issued = models.TextField(db_column='Date Issued', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    svc_description = models.TextField(db_column='Svc Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reported_by = models.TextField(db_column='Reported By', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    asset_id = models.TextField(db_column='Asset ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    work_order_field = models.TextField(db_column='Work Order #', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    airtable_id = models.TextField(blank=True, null=True)
    completed_by = models.TextField(db_column='Completed By', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mechanic_notes = models.TextField(db_column='Mechanic Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    hours_to_complete = models.FloatField(db_column='Hours-to-Complete', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date_completed = models.TextField(db_column='Date Completed', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    part_id = models.ForeignKey(Parts, models.DO_NOTHING, db_column='Part ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_id = models.ForeignKey(EquipmentList, models.DO_NOTHING, db_column='Equipment ID', to_field='Equipment ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    repair_import_staging = models.ForeignKey(RepairImportStaging, models.DO_NOTHING, db_column='Repair Import Staging')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'repair_history'

class SageImportStaging(models.Model):
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    mapped_description = models.TextField(db_column='Mapped Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapping_status = models.TextField(db_column='Mapping Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    imported_at = models.TextField(db_column='Imported At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    raw_json = models.TextField(db_column='Raw JSON', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    error_message = models.TextField(db_column='Error Message', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_filename = models.TextField(db_column='Source Filename', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    attachment_summary = models.TextField(db_column='Attachment Summary', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_batch_id = models.TextField(db_column='Import Batch ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_gl = models.TextField(db_column='Mapped GL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    row_number = models.FloatField(db_column='Row Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    promoted_at = models.TextField(db_column='Promoted At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_cost = models.FloatField(db_column='Mapped Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    mapped_date = models.TextField(db_column='Mapped Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sage_history_link = models.TextField(db_column='Sage History Link', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    promoted_field = models.IntegerField(db_column='Promoted?', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    import_notes = models.TextField(db_column='Import Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    promote_error = models.TextField(db_column='Promote Error', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'sage_import_staging'


class SageUploadIntake(models.Model):
    rows_created = models.BigIntegerField(db_column='Rows Created', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    source_filename = models.TextField(db_column='Source Filename', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_notes = models.TextField(db_column='Import Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    imported_at = models.TextField(db_column='Imported At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_batch_id = models.TextField(db_column='Import Batch ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    main_file = models.TextField(db_column='Main File', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parse_status = models.TextField(db_column='Parse Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    core_upload = models.TextField(db_column='Core upload', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'sage_upload_intake'

class SageHistory(models.Model):
    part_id = models.ForeignKey(Parts, models.DO_NOTHING, db_column='Part ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    unit_number_extracted_from_gl_number_field = models.TextField(db_column='Unit Number (Extracted from GL Number)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    sage_transaction_type = models.TextField(db_column='Sage Transaction Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sage_description = models.TextField(db_column='Sage Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    date = models.TextField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    general_ledger_number = models.TextField(db_column='General Ledger Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    supplier_information = models.TextField(db_column='Supplier Information', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    total_cost = models.FloatField(db_column='Total Cost', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sage_equipment = models.TextField(db_column='Sage Equipment', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_source = models.TextField(db_column='Data Source', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_batch_id = models.TextField(db_column='Import Batch ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sage_import_staging_id = models.ForeignKey(SageImportStaging, models.DO_NOTHING, db_column='Sage Import Staging ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    import_key = models.TextField(db_column='Import Key', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    part_description = models.TextField(db_column='Part Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'sage_history'

class Suppliers(models.Model):
    id = models.ForeignKey(Parts, models.DO_NOTHING, db_column='id', to_field='Supplier ID')
    supplier_name = models.TextField(db_column='Supplier Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    phone_number = models.TextField(db_column='Phone Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    contacts = models.TextField(db_column='Contacts', blank=True, null=True)  # Field name made lowercase.
    supplier_specialty = models.TextField(db_column='Supplier Specialty', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    supplier_location = models.TextField(db_column='Supplier Location', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    supplier_experience_notes = models.TextField(db_column='Supplier Experience Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    purchasing_notes = models.TextField(db_column='Purchasing Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    supplier_type = models.TextField(db_column='Supplier Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    website_url = models.TextField(db_column='Website URL', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    account_website_and_login_notes = models.TextField(db_column='Account, Website, and Login Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    credit_notes = models.TextField(db_column='Credit Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    attachments = models.TextField(db_column='Attachments', blank=True, null=True)  # Field name made lowercase.
    parts = models.TextField(db_column='Parts', blank=True, null=True)  # Field name made lowercase.
    vendor_rating = models.TextField(db_column='Vendor Rating', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    contact_notes = models.TextField(db_column='Contact Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    account_with_vendor = models.TextField(db_column='Account with Vendor', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    misc_notes = models.TextField(db_column='Misc. Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fax_number = models.TextField(db_column='Fax Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    last_purchase_date = models.TextField(db_column='Last Purchase Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    vendor_logs = models.TextField(db_column='Vendor Logs', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parts_2 = models.TextField(db_column='Parts 2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    parts_3 = models.TextField(db_column='Parts 3', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    address_1 = models.TextField(db_column='Address 1', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    address_2 = models.TextField(db_column='Address 2', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    city = models.TextField(db_column='City', blank=True, null=True)  # Field name made lowercase.
    zip_code = models.TextField(db_column='Zip Code', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status = models.TextField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    purchase_order_history = models.TextField(db_column='Purchase Order History', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    sage_history = models.TextField(db_column='Sage History', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    record_id = models.TextField(db_column='Record ID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    update_supplier_requests = models.TextField(db_column='Update Supplier Requests', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    office_cleaning_supplies = models.TextField(db_column='Office & Cleaning Supplies', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'suppliers'


class SuppliersLogs(models.Model):
    timestamp = models.TextField(db_column='Timestamp', blank=True, null=True)  # Field name made lowercase.
    log_entry = models.TextField(db_column='Log Entry', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    log_type = models.TextField(db_column='Log Type', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    user = models.TextField(db_column='User', blank=True, null=True)  # Field name made lowercase.
    supplier_name = models.TextField(db_column='Supplier Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Suppliers, models.DO_NOTHING, db_column='Supplier_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'suppliers_logs'

class UpdateEquipmentRequests(models.Model):
    new_status = models.TextField(db_column='New Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    equipment_link_field = models.TextField(db_column='Equipment (Link)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    applied = models.IntegerField(db_column='Applied', blank=True, null=True)  # Field name made lowercase.
    record_id_from_equipment_field = models.TextField(db_column='Record ID (from Equipment)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    submitted_at = models.TextField(db_column='Submitted At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_status = models.TextField(db_column='Final Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    target_record_id_resolved = models.TextField(db_column='Target Record ID Resolved', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    new_year = models.FloatField(db_column='New Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_year = models.FloatField(db_column='Final Year', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'update_equipment_requests'


class UpdatePartRequests(models.Model):
    final_part_description = models.TextField(db_column='Final Part Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    part_link_field = models.TextField(db_column='Part (Link)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    target_record_id_resolved = models.TextField(db_column='Target Record ID Resolved', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_part_description = models.TextField(db_column='New Part Description', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    submitted_at = models.TextField(db_column='Submitted At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    record_id_from_part_link_field = models.TextField(db_column='Record ID (from Part (Link))', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    airtable_id = models.TextField(blank=True, null=True)
    new_in_stock_location = models.TextField(db_column='New In-Stock Location', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_in_stock_location = models.TextField(db_column='Final In-Stock Location', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_status = models.TextField(db_column='Final Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_status = models.TextField(db_column='New Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_supplier_name = models.TextField(db_column='New Supplier Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_supplier_name = models.TextField(db_column='Final Supplier Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'update_part_requests'


class UpdateSupplierRequests(models.Model):
    supplier_link_field = models.TextField(db_column='Supplier (Link)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    submitted_at = models.TextField(db_column='Submitted At', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    target_record_id_resolved = models.TextField(db_column='Target Record ID Resolved', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_contact_name = models.TextField(db_column='Final Contact Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    applied = models.IntegerField(db_column='Applied', blank=True, null=True)  # Field name made lowercase.
    record_id_from_supplier_field = models.TextField(db_column='Record ID (from Supplier)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    new_contact_name = models.TextField(db_column='New Contact Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    airtable_id = models.TextField(blank=True, null=True)
    final_supplier_name = models.TextField(db_column='Final Supplier Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_contact_notes = models.TextField(db_column='Final Contact Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_phone = models.TextField(db_column='Final Phone', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_email = models.TextField(db_column='New Email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_status = models.TextField(db_column='New Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_phone = models.TextField(db_column='New Phone', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_misc_notes = models.TextField(db_column='New Misc Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_status = models.TextField(db_column='Final Status', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_supplier_notes = models.TextField(db_column='Final Supplier Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_email = models.TextField(db_column='Final Email', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_contact_notes = models.TextField(db_column='New Contact Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_supplier_notes = models.TextField(db_column='New Supplier Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    final_misc_notes = models.TextField(db_column='Final Misc Notes', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    new_supplier_name = models.TextField(db_column='New Supplier Name', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'update_supplier_requests'
