from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.datasets import Dataset
from datetime import datetime

# SAME dataset URI
sales_dataset = Dataset("mysql://warehouse/sales_table")

with DAG(
    dag_id="dataset_consumer_dag",
    start_date=datetime(2025, 12, 22),
    schedule=[sales_dataset],  # 👈 dataset-based scheduling
    catchup=False,
    tags=["dataset", "consumer"]
) as dag:

    consume_data = BashOperator(
        task_id="consume_sales_data",
        bash_command="echo 'Processing sales data'"
    )
