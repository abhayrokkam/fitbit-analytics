CREATE TABLE IF NOT EXISTS raw_data (
    client_id   VARCHAR(100)        NOT NULL,
    time        TIMESTAMPTZ         NOT NULL,
    metric      VARCHAR(100)        NOT NULL,
    value       DOUBLE PRECISION    NOT NULL
);
SELECT create_hypertable('raw_data', 'time', if_not_exists => TRUE);