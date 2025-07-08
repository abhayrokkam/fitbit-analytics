CREATE TABLE IF NOT EXISTS raw_data (
    time        TIMESTAMPTZ       NOT NULL,
    heart_rate  DOUBLE PRECISION
);
SELECT create_hypertable('raw_data', 'time', if_not_exists => TRUE);