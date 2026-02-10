import pandas as pd
import mysql.connector

def csv_to_raw():
    # CSV location inside Airflow container
    csv_path = "/opt/airflow/data/raw/Amazom.csv"

    # Load CSV
    df = pd.read_csv(csv_path)

    # MySQL connection (Docker service name)
    conn = mysql.connector.connect(
        host="mysql",  # ✅ IMPORTANT
        user="airflow_user",
        password="airflow_pass",
        database="amazon_db",
        port=3306
    )

    cursor = conn.cursor()

    insert_sql = """
        INSERT INTO raw_amazon (
            order_id, order_date, customer_id, customer_name,
            product_id, product_name, category, brand,
            quantity, unit_price, discount, tax,
            shipping_cost, total_amount, payment_method,
            order_status, city, state, country, seller_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Convert DataFrame to list of tuples (FAST)
    data = [tuple(row) for _, row in df.iterrows()]

    cursor.executemany(insert_sql, data)
    conn.commit()

    cursor.close()
    conn.close()

    print("✅ CSV successfully loaded into RAW layer")
