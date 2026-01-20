from airflow import DAG
from airflow.operators.subdag import SubDagOperator
from datetime import datetime

from etl_subdag import create_etl_subdag


with DAG(
    dag_id="parent_dag_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    etl_subdag_task = SubDagOperator(
        task_id="etl_subdag",
        subdag=create_etl_subdag(
            parent_dag_id="parent_dag_example",
            child_dag_id="etl_subdag",
            start_date=datetime(2024, 1, 1)
        )
    )
