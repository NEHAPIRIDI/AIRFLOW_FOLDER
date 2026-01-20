from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from datetime import datetime

def process_file():
    print("File found! Processing started.")

with DAG(
    dag_id="file_sensor_reschedule_mode",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    wait_for_file = FileSensor(
        task_id="wait_for_file",
        filepath="/opt/airflow/data/daily_data.csv",
        poke_interval=300,     # check every 5 minutes
        timeout=86400,        # wait up to 24 hours
        mode="reschedule"     # 🟢 RESCHEDULE MODE
    )

    process_task = PythonOperator(
        task_id="process_file",
        python_callable=process_file
    )

    wait_for_file >> process_task
