from celery import shared_task
from django.core.management import call_command


@shared_task
def scan_reorder_alerts_task():
    """
    Celery Beat entry point for the periodic low-stock scan. Delegates to the
    scan_reorder_alerts management command rather than duplicating its logic,
    so `python manage.py scan_reorder_alerts` and the scheduled task always
    behave identically.
    """
    call_command('scan_reorder_alerts')
