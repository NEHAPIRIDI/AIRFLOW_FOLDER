from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.datasets import Dataset
from datetime import datetime

# Define a dataset (this creates the dataset entry)
sales_dataset = Dataset("mysql://warehouse/sales_table")

with DAG(
    dag_id="dataset_producer_dag",
    start_date=datetime(2025, 12, 22),
    schedule=None,   # manual trigger
    catchup=False,
    tags=["dataset", "producer"]
) as dag:

    produce_data = BashOperator(
        task_id="produce_sales_data",
        bash_command="echo 'Sales data updated'",
        outlets=[sales_dataset]   # 👈 THIS LINE CREATES DATASET UPDATE
    )
