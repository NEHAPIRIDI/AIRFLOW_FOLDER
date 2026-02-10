from logger import get_connection

def get_pipeline_history(dag_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM etl_pipeline_history WHERE dag_name=%s",
        (dag_name,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
