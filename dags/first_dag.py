from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Function to run as a task
def hello_world():
    print("Hello, Airflow! Your first DAG is running.")

# Define the DAG
with DAG(
    dag_id="first_dag",
    start_date=datetime(2025, 12, 6),
    schedule_interval="@daily",  # Run once a day
    catchup=False
) as dag:

    # Define the task
    task1 = PythonOperator(
        task_id="print_hello",
        python_callable=hello_world
    )

    # Set task order (only one task here)
    task1
