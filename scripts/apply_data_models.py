import os
import mysql.connector

# -------------------------------------------------
# MYSQL CONNECTION CONFIG
# -------------------------------------------------
MYSQL_CONFIG = {
    "host": "mysql",              # Docker service name
    "user": "airflow_user",
    "password": "airflow_pass",
    "database": "amazon_db",
    "port": 3306
}

# -------------------------------------------------
# DATA MODELS BASE PATH (inside Airflow container)
# -------------------------------------------------
DATA_MODELS_PATH = "/opt/airflow/data_models"

# Order is IMPORTANT
MODEL_FOLDERS = [
    "raw",
    "staging",
    "curated",
    "lookups"
]


def execute_sql_file(cursor, file_path):
    """
    Reads and executes SQL statements from a file.
    """
    with open(file_path, "r") as f:
        sql_content = f.read()

    if not sql_content.strip():
        print(f"⚠️ Empty SQL file skipped: {file_path}")
        return

    print(f"▶ Applying model: {file_path}")

    statements = sql_content.split(";")
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)


def apply_data_models():
    """
    Applies all SQL files in data_models folders.
    """
    print("🚀 Starting data model application")

    conn = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = conn.cursor()

    for folder in MODEL_FOLDERS:
        folder_path = os.path.join(DATA_MODELS_PATH, folder)

        if not os.path.exists(folder_path):
            print(f"⚠️ Folder not found: {folder_path}")
            continue

        sql_files = sorted([
            f for f in os.listdir(folder_path) if f.endswith(".sql")
        ])

        for sql_file in sql_files:
            file_path = os.path.join(folder_path, sql_file)
            execute_sql_file(cursor, file_path)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ All data models applied successfully")


# -------------------------------------------------
# Allow manual execution
# -------------------------------------------------
if __name__ == "__main__":
    apply_data_models()
