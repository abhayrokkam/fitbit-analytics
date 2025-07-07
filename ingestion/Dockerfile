FROM python:3.12-slim-buster

WORKDIR /app

RUN apt-get update &&  apt-get install -y \
    postgresql-client \
    cron \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY ../pyproject.toml .
RUN pip install --no-cache-dir -r pyproject.toml

COPY ingest.py .

RUN echo "0 1 * * * python /app/ingest.py >> /proc/1/fd/1 2>> /proc/1/fd/2" > /etc/cron.d/fitbit-ingestion-cron \
    chmod 0644 /etc/cron.d/fitbit-ingestion-cron \
    crontab /etc/cron.d/fitbit-ingestion-cron

CMD ["cron", "-f"]