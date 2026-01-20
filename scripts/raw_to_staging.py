import mysql.connector

def raw_to_staging():
    conn = mysql.connector.connect(
        host="mysql",
        user="airflow_user",
        password="airflow_pass",
        database="amazon_db",
        port=3306
    )
    cursor = conn.cursor()

    # Ensure staging table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stg_amazon (
            order_id VARCHAR(50),
            order_date DATE,
            customer_id VARCHAR(50),
            customer_name VARCHAR(100),
            product_id VARCHAR(50),
            product_name VARCHAR(255),
            category VARCHAR(100),
            brand VARCHAR(100),
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
            seller_id VARCHAR(50)
        )
    """)

    cursor.execute("TRUNCATE TABLE stg_amazon")

    cursor.execute("""
        INSERT INTO stg_amazon (
            order_id, order_date, customer_id, customer_name,
            product_id, product_name, category, brand,
            quantity, unit_price, discount, tax,
            shipping_cost, total_amount, payment_method,
            order_status, city, state, country, seller_id
        )
        SELECT
            TRIM(order_id),

            CASE
                WHEN order_date LIKE '%-%' THEN STR_TO_DATE(order_date, '%Y-%m-%d')
                WHEN order_date LIKE '%/%' THEN STR_TO_DATE(order_date, '%m/%d/%Y')
                ELSE NULL
            END,

            TRIM(customer_id),
            UPPER(TRIM(customer_name)),

            TRIM(product_id),
            UPPER(TRIM(product_name)),
            UPPER(TRIM(category)),
            UPPER(TRIM(brand)),

            CAST(NULLIF(TRIM(quantity), '') AS UNSIGNED),
            CAST(NULLIF(TRIM(unit_price), '') AS DECIMAL(10,2)),
            CAST(NULLIF(TRIM(discount), '') AS DECIMAL(10,2)),
            CAST(NULLIF(TRIM(tax), '') AS DECIMAL(10,2)),
            CAST(NULLIF(TRIM(shipping_cost), '') AS DECIMAL(10,2)),
            CAST(NULLIF(TRIM(total_amount), '') AS DECIMAL(10,2)),

            UPPER(TRIM(payment_method)),
            UPPER(TRIM(order_status)),
            UPPER(TRIM(city)),
            UPPER(TRIM(state)),
            UPPER(TRIM(country)),
            TRIM(seller_id)

        FROM raw_amazon
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ RAW → STAGING completed successfully")
