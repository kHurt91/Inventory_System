#!/bin/sh
set -e

echo "Waiting for database at ${DB_HOST:-db}:${DB_PORT:-3306}..."
until python - <<'PYEOF'
import os
import socket
import sys

host = os.environ.get("DB_HOST", "db")
port = int(os.environ.get("DB_PORT", "3306"))
try:
    with socket.create_connection((host, port), timeout=2):
        pass
except OSError:
    sys.exit(1)
PYEOF
do
  sleep 2
done
echo "Database is reachable."

# Only managed models (django's own apps, django_celery_beat, PurchaseOrder/
# PurchaseOrderLine) have real migrations -- the legacy inventory tables are
# managed=False and must already exist in the target database (restored from
# a dump) before this runs.
python manage.py migrate --noinput

exec "$@"
