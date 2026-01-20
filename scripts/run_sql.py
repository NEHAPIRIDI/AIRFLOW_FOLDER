def run_sql_file(sql_path):
    import mysql.connector  # ✅ moved inside function

    conn = mysql.connector.connect(
        host="mysql",
        user="airflow_user",
        password="airflow_pass",
        database="amazon_db",
        port=3306
    )
    cursor = conn.cursor()

    with open(sql_path, "r") as f:
        sql = f.read()

    for statement in sql.split(";"):
        if statement.strip():
            cursor.execute(statement)

    conn.commit()
    cursor.close()
    conn.close()
