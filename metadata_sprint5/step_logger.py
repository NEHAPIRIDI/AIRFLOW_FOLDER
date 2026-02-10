from datetime import datetime
from logger import get_connection

def log_step_start(run_id, step_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO etl_step_runs
        (run_id, step_name, start_time, status)
        VALUES (%s,%s,%s,'RUNNING')""",
        (run_id, step_name, datetime.now())
    )
    conn.commit()
    conn.close()

def log_step_end(run_id, step_name, status, records, error=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE etl_step_runs
        SET end_time=%s,
            status=%s,
            records_processed=%s,
            error_message=%s
        WHERE run_id=%s AND step_name=%s""",
        (datetime.now(), status, records, error, run_id, step_name)
    )
    conn.commit()
    conn.close()
