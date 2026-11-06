# API image — FastAPI behind nginx (see docker-compose.yml).
# Python 3.11: the version the test suite runs on.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# mysqldump is needed by the scheduled database backups (app/backups).
# PyMySQL is pure Python: no compiler or MySQL client library required.
RUN apt-get update \
    && apt-get install -y --no-install-recommends default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Unprivileged user; uploads/ and backups/ are mounted volumes it must own.
RUN useradd --create-home --uid 1000 app \
    && mkdir -p uploads/images uploads/cvs uploads/videos backups \
    && chown -R app:app /app
USER app

EXPOSE 8000
ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
