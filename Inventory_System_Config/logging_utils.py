import json
import logging


class JsonFormatter(logging.Formatter):
    """Renders each log record as a single JSON line, for container/log-aggregator consumption."""

    def format(self, record):
        payload = {
            'timestamp': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        if record.exc_info:
            payload['exc_info'] = self.formatException(record.exc_info)
        # django.request's log records carry a real HttpRequest on `.request` -- not
        # JSON-serializable directly, so pull out just the path, not the raw object.
        request = getattr(record, 'request', None)
        if request is not None:
            payload['path'] = getattr(request, 'path', None)
        if hasattr(record, 'status_code'):
            payload['status_code'] = record.status_code
        return json.dumps(payload)
