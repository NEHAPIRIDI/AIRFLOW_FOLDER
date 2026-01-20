-- CURATED layer
-- Analytics-ready data

CREATE TABLE IF NOT EXISTS cur_amazon (
    order_id VARCHAR(50),
    customer_id VARCHAR(50),
    product_id VARCHAR(50),
    category VARCHAR(100),
    seller_id VARCHAR(50),
    order_date DATE,
    load_date DATE,
    quantity INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(10,2),
    tax DECIMAL(10,2),
    shipping_cost DECIMAL(10,2),
    total_amount DECIMAL(10,2),
    payment_method VARCHAR(50),
    order_status VARCHAR(50),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    is_current BOOLEAN
);
