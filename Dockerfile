FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# mysqlclient needs these to build against MySQL; kept in the final image too
# since mysqlclient links against libmariadb at runtime, not just build time.
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --system --deploy

COPY . .

# chmod explicitly rather than relying on the host's executable bit surviving
# COPY -- NTFS (Windows build hosts) doesn't track it the way Docker expects.
RUN chmod +x docker/entrypoint.sh \
    && useradd --create-home --uid 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["./docker/entrypoint.sh"]
CMD ["gunicorn", "-c", "docker/gunicorn.conf.py", "Inventory_System_Config.wsgi:application"]
