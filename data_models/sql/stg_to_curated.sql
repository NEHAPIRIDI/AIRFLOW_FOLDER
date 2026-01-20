INSERT INTO cur_amazon (
    order_id, customer_id, product_id, category, seller_id,
    order_date, load_date,
    quantity, unit_price, discount, tax,
    shipping_cost, total_amount,
    payment_method, order_status,
    city, state, country,
    is_current
)
WITH base_data AS (
    SELECT
        order_id,
        customer_id,
        product_id,
        UPPER(category) AS category_raw,
        seller_id,
        DATE(order_date) AS order_date,
        quantity,
        unit_price,
        discount,
        tax,
        shipping_cost,
        total_amount,
        payment_method,
        order_status,
        city,
        state,
        country
    FROM stg_amazon
),
final_data AS (
    SELECT
        order_id,
        customer_id,
        product_id,
        category_raw AS category,
        seller_id,
        order_date,
        CURRENT_DATE AS load_date,
        quantity,
        unit_price,
        discount,
        tax,
        shipping_cost,
        total_amount,
        payment_method,
        order_status,
        city,
        state,
        country,
        TRUE AS is_current
    FROM base_data
)
SELECT
    order_id, customer_id, product_id, category, seller_id,
    order_date, load_date,
    quantity, unit_price, discount, tax,
    shipping_cost, total_amount,
    payment_method, order_status,
    city, state, country,
    is_current
FROM final_data;
