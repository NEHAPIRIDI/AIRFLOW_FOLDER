from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def create_etl_subdag(parent_dag_id, child_dag_id, start_date):
    """
    This function creates a SubDAG
    """

    dag_id = f"{parent_dag_id}.{child_dag_id}"

    subdag = DAG(
        dag_id=dag_id,
        start_date=start_date,
        schedule_interval=None,
        catchup=False
    )

    # -------------------------
    # SubDAG Tasks
    # -------------------------
    extract = PythonOperator(
        task_id="extract",
        python_callable=lambda: print("Extracting data"),
        dag=subdag
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=lambda: print("Transforming data"),
        dag=subdag
    )

    load = PythonOperator(
        task_id="load",
        python_callable=lambda: print("Loading data"),
        dag=subdag
    )

    # Task order inside SubDAG
    extract >> transform >> load

    return subdag
