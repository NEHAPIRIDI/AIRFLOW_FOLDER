import mysql.connector
from datetime import datetime

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="nehadatabase"
    )

def log_dag_start(run_id, dag_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO etl_dag_runs VALUES (%s,%s,%s,NULL,'RUNNING')",
        (run_id, dag_name, datetime.now())
    )
    conn.commit()
    conn.close()

def log_dag_end(run_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE etl_dag_runs SET end_time=%s, status=%s WHERE run_id=%s",
        (datetime.now(), status, run_id)
    )
    conn.commit()
    conn.close()
