FROM python:3.12-slim

# Working Directory
WORKDIR /app

# Update apt and install cron, remove apt lists
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# First, install libraries for caching
COPY pyproject.toml .
RUN pip install .

# Copying files 
COPY ingestion/ingest.py .
COPY modules/ ./modules
COPY .env .env
COPY ingestion/cronjob /etc/cron.d/daily-cron

# Permissions
RUN chmod 0644 /etc/cron.d/daily-cron

# Load the job
RUN crontab /etc/cron.d/daily-cron

# Start cron daemon in foreground
CMD ["cron", "-f"]