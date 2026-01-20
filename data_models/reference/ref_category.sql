CREATE TABLE IF NOT EXISTS ref_category (
    source_category VARCHAR(100) PRIMARY KEY,
    standard_category VARCHAR(100),
    updated_at TIMESTAMP
);
