from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime


# Simple function for all tasks
def print_message(message):
    print(message)


# Define the DAG
with DAG(
    dag_id="task_group_example",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,   # Run manually
    catchup=False
) as dag:

    # -------------------------------
    # Extract Task Group
    # -------------------------------
    with TaskGroup(group_id="extract_group") as extract_group:

        extract_users = PythonOperator(
            task_id="extract_users",
            python_callable=print_message,
            op_args=["Extracting users data"]
        )

        extract_orders = PythonOperator(
            task_id="extract_orders",
            python_callable=print_message,
            op_args=["Extracting orders data"]
        )

    # -------------------------------
    # Transform Task Group
    # -------------------------------
    with TaskGroup(group_id="transform_group") as transform_group:

        transform_users = PythonOperator(
            task_id="transform_users",
            python_callable=print_message,
            op_args=["Transforming users data"]
        )

        transform_orders = PythonOperator(
            task_id="transform_orders",
            python_callable=print_message,
            op_args=["Transforming orders data"]
        )

    # -------------------------------
    # Load Task Group
    # -------------------------------
    with TaskGroup(group_id="load_group") as load_group:

        load_users = PythonOperator(
            task_id="load_users",
            python_callable=print_message,
            op_args=["Loading users data"]
        )

        load_orders = PythonOperator(
            task_id="load_orders",
            python_callable=print_message,
            op_args=["Loading orders data"]
        )

    # -------------------------------
    # Set dependencies between groups
    # -------------------------------
    extract_group >> transform_group >> load_group
