from logger import get_connection

def get_failed_runs():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM etl_dag_runs WHERE status='FAILED'"
    )
    data = cursor.fetchall()
    conn.close()
    return data

def get_step_metrics(run_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT step_name, records_processed, status FROM etl_step_runs WHERE run_id=%s",
        (run_id,)
    )
    result = cursor.fetchall()
    conn.close()
    return result
