-- Lookup table for category standardization

CREATE TABLE IF NOT EXISTS lkp_category (
    source_category VARCHAR(100),
    standardized_category VARCHAR(100),
    is_active BOOLEAN
);
