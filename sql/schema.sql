-- Warehouse schema for the crypto ETL pipeline.
-- Run once before the first load: psql -d crypto_db -f sql/schema.sql
-- (load.py also auto-creates the table via to_sql, but explicit DDL documents
--  the contract and lets you add types / constraints intentionally.)

CREATE TABLE IF NOT EXISTS fact_coin_price (
    id                            TEXT,
    symbol                        TEXT,
    name                          TEXT,
    current_price                 NUMERIC,
    market_cap                    BIGINT,
    total_volume                  BIGINT,
    price_change_percentage_24h   NUMERIC,
    price_change_percentage_7d    NUMERIC,
    is_volatile_24h               BOOLEAN,
    last_updated                  TIMESTAMPTZ,
    loaded_at                     TIMESTAMPTZ DEFAULT now()
);

-- Speeds up the "latest rows" and per-coin time-series queries.
CREATE INDEX IF NOT EXISTS idx_fact_coin_price_id_time
    ON fact_coin_price (id, last_updated DESC);
