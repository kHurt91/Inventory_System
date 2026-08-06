# Database seed directory

Place a full `mysqldump` of `inventory_db` here (e.g. copy one of the
`backup_*.sql` files from the project root) before running
`docker compose up` for the first time.

The official `mysql` image executes every `.sql`/`.sh` file in this directory,
in filename order, exactly once -- only when the `db_data` volume is empty
(a fresh environment). This is required because the legacy inventory tables
(`parts`, `suppliers`, `equipment_list`, etc.) are `managed = False` in
Django -- no migration creates them, so a fresh container has no way to get
that schema/data other than restoring a dump here.

`django.contrib.*`, `django_celery_beat`, and `PurchaseOrder`/
`PurchaseOrderLine` are real Django-managed migrations and don't need
anything here -- `docker/entrypoint.sh` runs `manage.py migrate` on every
container start regardless.
