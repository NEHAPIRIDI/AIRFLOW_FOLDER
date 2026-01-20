import mysql.connector
from datetime import date
from fuzzy_mapper import fuzzy_match

def staging_to_curated():
    BATCH_SIZE = 500

    conn = mysql.connector.connect(
        host="mysql",
        user="airflow_user",
        password="airflow_pass",
        database="amazon_db",
        port=3306
    )
    cursor = conn.cursor(dictionary=True)

    # -----------------------------
    # CREATE CURATED TABLE IF MISSING
    # -----------------------------
    cursor.execute("""
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
        )
    """)

    # -----------------------------
    # FETCH STAGING DATA
    # -----------------------------
    cursor.execute("SELECT * FROM stg_amazon")
    rows = cursor.fetchall()

    if not rows:
        print("⚠️ No data in STAGING — skipping CURATED")
        return

    cursor.execute("TRUNCATE TABLE cur_amazon")

    # -----------------------------
    # LOAD LOOKUP SAFELY
    # -----------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lkp_category (
            source_category VARCHAR(100),
            standardized_category VARCHAR(100),
            is_active BOOLEAN
        )
    """)

    cursor.execute("""
        SELECT source_category, standardized_category
        FROM lkp_category
        WHERE is_active = TRUE
    """)

    lookup_rows = cursor.fetchall()

    category_lookup = {
        r["source_category"].upper(): r["standardized_category"]
        for r in lookup_rows
    }

    standard_categories = list(set(category_lookup.values()))

    # -----------------------------
    # PREPARE DATA
    # -----------------------------
    batch_data = []

    for r in rows:
        raw_cat = r["category"] or ""
        raw_upper = raw_cat.upper()

        if raw_upper in category_lookup:
            final_category = category_lookup[raw_upper]
        elif standard_categories:
            final_category = fuzzy_match(raw_upper, standard_categories) or raw_cat
        else:
            final_category = raw_cat

        batch_data.append((
            r["order_id"],
            r["customer_id"],
            r["product_id"],
            final_category.title(),
            r["seller_id"],
            r["order_date"],
            date.today(),
            r["quantity"],
            r["unit_price"],
            r["discount"],
            r["tax"],
            r["shipping_cost"],
            r["total_amount"],
            r["payment_method"],
            r["order_status"],
            r["city"],
            r["state"],
            r["country"],
            True
        ))

    insert_sql = """
        INSERT INTO cur_amazon VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
            %s,%s,%s,%s,%s,%s,%s,%s,%s
        )
    """

    for i in range(0, len(batch_data), BATCH_SIZE):
        cursor.executemany(insert_sql, batch_data[i:i+BATCH_SIZE])
        conn.commit()

    cursor.close()
    conn.close()

    print(f"✅ STAGING → CURATED completed ({len(batch_data)} rows)")
