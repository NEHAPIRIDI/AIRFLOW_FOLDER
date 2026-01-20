from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner": "you", "retries": 2, "retry_delay": timedelta(minutes=1)}

with DAG(
    dag_id="example_bash_dag",
    default_args=default_args,
    description="Example Airflow DAG",
    start_date=datetime(2025, 12, 19),
    schedule_interval=None,
    catchup=False,
    tags=["example"]
) as dag:
    t1 = BashOperator(task_id="print_date", bash_command="date")
    t2 = BashOperator(task_id="print_msg", bash_command="echo hello world")
    t3 = BashOperator(task_id="sleep", bash_command="sleep 3")
    t1 >> t2 >>t3
