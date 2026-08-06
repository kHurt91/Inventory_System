import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Inventory_System_Config.settings')

app = Celery('Inventory_System_Config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
