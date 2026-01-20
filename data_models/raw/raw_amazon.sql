-- RAW layer table
-- Source-aligned Amazon CSV data

CREATE TABLE IF NOT EXISTS raw_amazon (
    order_id VARCHAR(50),
    order_date VARCHAR(50),
    customer_id VARCHAR(50),
    customer_name VARCHAR(100),
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    brand VARCHAR(100),
    quantity VARCHAR(20),
    unit_price VARCHAR(20),
    discount VARCHAR(20),
    tax VARCHAR(20),
    shipping_cost VARCHAR(20),
    total_amount VARCHAR(20),
    payment_method VARCHAR(50),
    order_status VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    seller_id VARCHAR(50)
);
