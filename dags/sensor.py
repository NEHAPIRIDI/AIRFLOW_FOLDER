from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from datetime import datetime

def process_file():
    print("File found! Processing started.")

with DAG(
    dag_id="file_sensor_poke_mode",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath="/opt/airflow/data/input.csv",
        poke_interval=30,     # check every 30 seconds
        timeout=300,          # wait max 5 minutes
        mode="poke"           # 🔴 POKE MODE
    )

    process_task = PythonOperator(
        task_id="process_file",
        python_callable=process_file
    )

    wait_for_file >> process_task
