SELECT
    (SELECT COUNT(*) FROM raw_amazon)  AS raw_count,
    (SELECT COUNT(*) FROM stg_amazon)  AS staging_count,
    (SELECT COUNT(*) FROM cur_amazon)  AS curated_count;
