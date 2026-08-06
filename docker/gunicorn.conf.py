import multiprocessing
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
threads = int(os.environ.get('GUNICORN_THREADS', 2))
timeout = int(os.environ.get('GUNICORN_TIMEOUT', 30))

# Plain stdout/stderr -- the container runtime/log aggregator captures these;
# Django's own JSON-formatted app logs (see LOGGING in settings.py) also go
# to stdout, so both streams end up in the same collected log sink.
accesslog = '-'
errorlog = '-'
