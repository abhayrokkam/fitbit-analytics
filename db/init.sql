CREATE TABLE IF NOT EXISTS hr_data (
    time        TIMESTAMPTZ       NOT NULL,
    heart_rate  DOUBLE PRECISION
);
SELECT create_hypertable('hr_data', 'time', if_not_exists => TRUE);