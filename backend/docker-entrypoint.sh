#!/bin/sh
# Container start: bring the schema up to date, then serve the API.
set -e

echo "Migrations de la base (alembic upgrade head)…"
alembic upgrade head

# --proxy-headers: trust X-Forwarded-For from nginx so rate limiting sees the
# real visitor IP. Only nginx can reach this port (internal Docker network).
exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --proxy-headers \
  --forwarded-allow-ips "*"
