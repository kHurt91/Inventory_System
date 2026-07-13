# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AssetEquipmentMapping(models.Model):
    last_updated = models.TextField(blank=True, null=True)
    asset = models.ForeignKey('EquipmentList', models.DO_NOTHING, blank=True, null=True)
    equipment = models.ForeignKey('EquipmentList', models.DO_NOTHING, related_name='assetequipmentmapping_equipment_set', blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    equipment_list_2 = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.asset}-{self.equipment}-{self.active}"

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
    name = models.TextField(blank=True, null=True)
    build_sheet = models.TextField(blank=True, null=True)
    equipment = models.ForeignKey('EquipmentList', models.DO_NOTHING, blank=True, null=True)
    

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
    record_id = models.IntegerField(blank=True, null=True)
    make = models.TextField(blank=True, null=True)
    model = models.TextField(blank=True, null=True)
    owned_by = models.TextField(blank=True, null=True)
    year = models.SmallIntegerField(blank=True, null=True)
    asset_category = models.TextField(blank=True, null=True)
    equipment_id = models.IntegerField(blank=True, null=True)
    serial_number = models.TextField(blank=True, null=True)
    equipment_notes = models.TextField(blank=True, null=True)
    part_compatibility = models.TextField(blank=True, null=True)
    tires = models.TextField(blank=True, null=True)
    manuals = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    build_sheet = models.IntegerField(blank=True, null=True)
    asset_id = models.IntegerField(blank=True, null=True)
    alt_asset_id = models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.equipment_id} - {self.make} {self.model}"

    class Meta:
        managed = False
        db_table = 'equipment_list'


class InventoryTransactions(models.Model):
    signed_quantity = models.BigIntegerField(blank=True, null=True)
    transaction_type = models.TextField(blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    quantity = models.BigIntegerField(blank=True, null=True)
    part = models.ForeignKey('Parts', models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return f"{self.part}-{self.transaction_type}{self.signed_quantity}"

    class Meta:
        managed = False
        db_table = 'inventory_transactions'


class OfficeAndCleaningSupplies(models.Model):
    status = models.TextField(blank=True, null=True)
    minimum_quantity = models.BigIntegerField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    in_stock_location = models.TextField(blank=True, null=True)
    office_supply_transactions = models.TextField(blank=True, null=True)
    on_hand = models.BigIntegerField(blank=True, null=True)
    supply_name = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, blank=True, null=True)
    
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
    supply_name = models.TextField(blank=True, null=True)
    transaction_type = models.TextField(blank=True, null=True)
    office_supply = models.ForeignKey(OfficeAndCleaningSupplies, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'office_supply_transactions'


class Parts(models.Model):
    part_description = models.TextField(blank=True, null=True)
    in_stock_location = models.TextField(blank=True, null=True)
    on_hand = models.BigIntegerField(blank=True, null=True)
    equipment_fitment = models.TextField(blank=True, null=True)
    part_id = models.AutoField(primary_key=True)
    record_id = models.IntegerField(blank=True, null=True)
    needs_reorder = models.IntegerField(blank=True, null=True)
    manufacturer = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, blank=True, null=True, related_name='supplied_parts')
    alternate_supplier = models.TextField(blank=True, null=True)
    cost_notes = models.TextField(blank=True, null=True)
    brand_model = models.TextField(blank=True, null=True)
    part_name = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.part_description} Part ID:{self.part_id}"

    class Meta:
        managed = False
        db_table = 'parts'


class PartsDiagrams(models.Model):
    notes = models.TextField(blank=True, null=True)
    attachments = models.TextField(blank=True, null=True)
    equipment = models.ForeignKey(EquipmentList, models.DO_NOTHING, blank=True, null=True)
    diagram_description = models.TextField(blank=True, null=True)
    component_part_id = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parts_diagrams'


class PartsHasEquipmentList(models.Model):
    pk = models.CompositePrimaryKey('parts_part_id', 'equipment_list_id')
    parts_part = models.ForeignKey(Parts, models.DO_NOTHING)
    equipment_list = models.ForeignKey(EquipmentList, models.DO_NOTHING)
    
    def __str__(self):
        return f"Part:{self.parts_part.part_id} Equipment:{self.equipment_list.equipment_id}"

    class Meta:
        managed = False
        db_table = 'parts_has_equipment_list'


class PartsSuppliers(models.Model):
    pk = models.CompositePrimaryKey('part_id', 'supplier_id')
    part = models.ForeignKey(Parts, models.DO_NOTHING)
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING)
    supplier_part_code = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return f"{self.pk}"

    class Meta:
        managed = False
        db_table = 'parts_suppliers'


class PurchaseOrderHistory(models.Model):
    part_description = models.TextField(blank=True, null=True)
    part = models.ForeignKey(Parts, models.DO_NOTHING, blank=True, null=True)
    date_issued = models.DateField(blank=True, null=True)
    invoice_number = models.DecimalField(max_digits=22, decimal_places=1, blank=True, null=True)
    po_number = models.TextField(blank=True, null=True)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    company = models.TextField(blank=True, null=True)
    supplier = models.TextField(blank=True, null=True)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    received_date = models.DateField(blank=True, null=True)
    issued_by = models.TextField(blank=True, null=True)
    shipper_packing_slip_number = models.TextField(blank=True, null=True)
    equipment = models.ForeignKey(EquipmentList, models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return f"Part:{self.part.part_id} Date received:{self.received_date}"

    class Meta:
        managed = False
        db_table = 'purchase_order_history'


class RepairHistory(models.Model):
    date_needed = models.DateField(blank=True, null=True)
    date_issued = models.DateField(blank=True, null=True)
    svc_description = models.TextField(blank=True, null=True)
    reported_by = models.TextField(blank=True, null=True)
    asset_id = models.TextField(blank=True, null=True)
    work_order_number = models.TextField(blank=True, null=True)
    completed_by = models.TextField(blank=True, null=True)
    mechanic_notes = models.TextField(blank=True, null=True)
    hours_to_complete = models.FloatField(blank=True, null=True)
    date_completed = models.DateField(blank=True, null=True)
    part = models.ForeignKey(Parts, models.DO_NOTHING, blank=True, null=True)
    equipment = models.ForeignKey(EquipmentList, models.DO_NOTHING, blank=True, null=True)
    
    def __str__(self):
        return f"Equipment:{self.equipment.equipment_id} Date Issued:{self.date_issued} Date Completed:{self.date_completed}"

    class Meta:
        managed = False
        db_table = 'repair_history'


class SageHistory(models.Model):
    part = models.ForeignKey(Parts, models.DO_NOTHING, blank=True, null=True)
    unit_number = models.TextField(blank=True, null=True)
    sage_transaction_type = models.TextField(blank=True, null=True)
    sage_description = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    general_ledger_number = models.TextField(blank=True, null=True)
    supplier_information = models.TextField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    sage_equipment = models.TextField(blank=True, null=True)
    data_source = models.TextField(blank=True, null=True)
    import_batch_id = models.TextField(blank=True, null=True)
    import_key = models.TextField(blank=True, null=True)
    part_description = models.TextField(blank=True, null=True)
    

    class Meta:
        managed = False
        db_table = 'sage_history'


class Suppliers(models.Model):
    supplier_name = models.TextField(blank=True, null=True)
    phone_number = models.TextField(blank=True, null=True)
    contacts = models.TextField(blank=True, null=True)
    supplier_specialty = models.TextField(blank=True, null=True)
    supplier_location = models.TextField(blank=True, null=True)
    supplier_experience_notes = models.TextField(blank=True, null=True)
    purchasing_notes = models.TextField(blank=True, null=True)
    supplier_type = models.TextField(blank=True, null=True)
    website_url = models.TextField(blank=True, null=True)
    account_website_login_notes = models.TextField(blank=True, null=True)
    credit_notes = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    attachments = models.TextField(blank=True, null=True)
    parts = models.TextField(blank=True, null=True)
    vendor_rating = models.TextField(blank=True, null=True)
    contact_notes = models.TextField(blank=True, null=True)
    account_with_vendor = models.TextField(blank=True, null=True)
    misc_notes = models.TextField(blank=True, null=True)
    fax_number = models.TextField(blank=True, null=True)
    last_purchase_date = models.DateField(blank=True, null=True)
    vendor_logs = models.TextField(blank=True, null=True)
    parts_2 = models.TextField(blank=True, null=True)
    parts_3 = models.TextField(blank=True, null=True)
    address_1 = models.TextField(blank=True, null=True)
    address_2 = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    zip_code = models.TextField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    purchase_order_history = models.IntegerField(blank=True, null=True)
    record_id = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Supplier {self.supplier_name}"

    class Meta:
        managed = False
        db_table = 'suppliers'


class SuppliersLogs(models.Model):
    time_stamp = models.TextField(blank=True, null=True)
    log_entry = models.TextField(blank=True, null=True)
    log_type = models.TextField(blank=True, null=True)
    user = models.TextField(blank=True, null=True)
    supplier_name = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Suppliers, models.DO_NOTHING, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'suppliers_logs'