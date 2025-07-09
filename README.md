# Fitbit Data Analytics

This project focuses on building core components of a software platform that enables ETL (Extract, Transform, Load) of wearable device data - specifically from the Fitbit Charge - for use in clinical trials. Our goal is to empower researchers and clinicians with tools to manage and analyze time-series health data collected from up to 1,000 participants.

Key objectives include:

- Developing robust, distributed software infrastructure to support clinical trials at scale.
- Creating intuitive dashboards for real-time visualization and analysis of wearable data.
- Designing extensible data schemas that support integration with various wearable devices.

The Fitbit Charge provides high-resolution intraday data (up to 1-second intervals), which must be ingested, transformed, and replicated to Stanford’s cloud-hosted servers. The processed data is then accessed by a web application designed for clinical trial managers to monitor participants.

---

- [Fitbit Data Analytics](#fitbit-data-analytics)
- [Phase 1: Ingestion Flow](#phase-1-ingestion-flow)
  - [Why TimescaleDB?](#why-timescaledb)
  - [Architecture](#architecture)
  - [Database Schema](#database-schema)
  - [Guide to Code](#guide-to-code)
    - [Prerequisites:](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)

# Phase 1: Ingestion Flow

## Why TimescaleDB?

This project uses TimescaleDB, a PostgreSQL extension that supercharges it for time-series data. For an application like Fitbit data analysis, a time-series database is superior to a traditional relational database for several key reasons:

- Performance at Scale: TimescaleDB automatically partitions data by time into smaller, more manageable chunks called "hypertables". This partitioning significantly speeds up queries on large time-series datasets, as the database engine only needs to scan the relevant time chunks instead of the entire table. You can see this in action in the db/init.sql file with the create_hypertable function.

- Optimized for Ingestion: Time-series databases are built for high write throughput, which is essential for ingesting streams of data like heart rate measurements collected throughout the day.

- Built-in Time-Oriented Functions: TimescaleDB provides a rich set of specialized SQL functions for time-series analysis (e.g., time_bucket, first, last), simplifying complex queries like downsampling, gap-filling, and calculating moving averages.

- Scalability and Compression: As data grows, TimescaleDB offers native, columnar compression to reduce storage costs by up to 90% without sacrificing query speed. It also supports scalable clustering to handle massive datasets.

## Architecture

The pipeline is coordinated by Docker Compose and consists of two main services:

1. `ingestion`: A Python container responsible for fetching and writing data.
   
   - Cron Scheduler: A `cron` process runs inside the container, triggering the ingestion script once daily at 6:00 AM, as defined in `ingestion/cronjob`.

    - Ingestion Script (`ingest.py`): This Python script uses the `wearipedia` library to connect to the Fitbit API. It reads a `last_run.json` timestamp to fetch only the previous day's data (delta-load), preventing duplicate records. It then writes the heart rate data into the `timescaledb` service.

    - Logging: The script uses a robust logging configuration (`modules/logging_config.py`) that outputs logs to both the console and a rotating log file (`app.log`).

2. `timescaledb`: The time-series database service.

   - Official Image: Uses the official `timescale/timescaledb:latest-pg16` image from Docker Hub.

    - Persistent Storage: A Docker volume is mounted to `./data/timescaledb`, ensuring that all database data persists even if the container crashes or is restarted.

    - Initialization: On the first run, it executes `db/init.sql` to create the `raw_data` hypertable.

The two services communicate over a Docker network, with the `ingestion` service connecting to the `timescaledb` service using the hostname `timescaledb`.

## Database Schema

The data is stored in a single TimescaleDB hypertable named `raw_data`.

File: `db/init.sql`

```sql
CREATE TABLE IF NOT EXISTS raw_data (
    time        TIMESTAMPTZ       NOT NULL,
    heart_rate  DOUBLE PRECISION
);
SELECT create_hypertable('raw_data', 'time', if_not_exists => TRUE);
```

- `time` (TIMESTAMPTZ): The primary key for the hypertable. This column stores the precise timestamp for each heart rate measurement with time zone information. The table is partitioned based on this column.

- `heart_rate` (DOUBLE PRECISION): Stores the beats-per-minute value for the corresponding timestamp.

## Guide to Code

Follow these instructions to get the project up and running locally.

### Prerequisites:

- Docker: [Install Docker](https://docs.docker.com/engine/install/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. Clone the Repository

    ```bash
    git clone https://github.com/abhayrokkam/fitbit-analytics.git
    cd fitbit-analytics
    ```

2. Configure Environment Variables

    Create a `.env` file by copying the example file.

    ```bash
    cp .env.example .env
    ```
    Now, open the `.env` file and fill in the required values.

3. Setup the Fitbit API Credentials

    By default, the project uses synthetic data (`SYNTHETIC=True`). To use your own Fitbit data:

    - Set `SYNTHETIC=False` in your `.env` file.

    - You will need to obtain API credentials. Follow an official Fitbit guide to get your `CLIENT_ID`, `CLIENT_SECRET`, and an initial `ACCESS_TOKEN`. Add these to your `.env` file.

4. Build and Run the Containers

    Use Docker Compose to build the images and start the services in detached mode.

    ```bash
    docker-compose up --build -d
    ```
    This command will:
    - Build the `ingestion` service Docker images.
    - Pull the `timescaledb` image.
    - STart both containers. The ingestion container will wait until its scheduled cron time to run the script.

5. Verify the Setup
    
    You can check the logs to see the output from the services.
    
    ```bash
    # Logs of ingestion service
    docker-compose logs -f ingestion

    # Logs for the database
    docker-compose logs -f timescaledb
    ``` 
    To connect to the databse directly, you can use a PostgreSQL client like `psql`.

### Configuration

All configurations are managed through the `.env` file.

| Variable      | Description    | Example        |
|:-------------:|:---------------|:--------------:|
|DB_NAME    |The name of the PostgreSQL database.|  your-db-name
|DB_USER    |The username for the PostgreSQL database.| your-username
|DB_PASS    |The password for the PostgreSQL user.| your-password
|DB_HOST    |The hostname of the database service.| localhost
|DB_PORT    |The internal port the database is running on within the Docker network.|   5432
|CLIENT_ID  |Your Fitbit application's Client ID. (Required if SYNTHETIC=False).|   ABC123
|CLIENT_SECRET  |Your Fitbit application's Client Secret. (Required if SYNTHETIC=False).|   abcd1234
|ACCESS_TOKEN   |An OAuth 2.0 access token for the Fitbit API. (Required if SYNTHETIC=False).| your-long-access-token
|SYNTHETIC   |A boolean flag to control the data source. Set to True to use sample data from the wearipedia library or False to pull from the live Fitbit API.|  True