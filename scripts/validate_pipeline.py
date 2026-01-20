import mysql.connector

def validate_pipeline():
    conn = mysql.connector.connect(
        host="mysql",
        user="airflow_user",
        password="airflow_pass",
        database="amazon_db",
        port=3306
    )
    cursor = conn.cursor()

    checks = {
        "raw": "SELECT COUNT(*) FROM raw_amazon",
        "stg": "SELECT COUNT(*) FROM stg_amazon",
        "cur": "SELECT COUNT(*) FROM cur_amazon"
    }

    counts = {}

    for k, q in checks.items():
        cursor.execute(q)
        counts[k] = cursor.fetchone()[0]

    print("🔍 ETL COUNTS:", counts)

    if counts["stg"] > counts["raw"]:
        raise ValueError("❌ STAGING has more rows than RAW")

    cursor.close()
    conn.close()

    print("✅ Pipeline validation passed")
