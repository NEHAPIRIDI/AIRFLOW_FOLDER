import sys
import os
sys.path.append("/opt/airflow/scripts")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from csv_to_raw import csv_to_raw
from raw_to_staging import raw_to_staging
from staging_to_curated import staging_to_curated
from validate_pipeline import validate_pipeline

default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="amazon_etl_pipeline",
    description="Amazon CSV ETL Pipeline (RAW → STAGING → CURATED)",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["amazon", "etl"],
) as dag:

    csv_to_raw_task = PythonOperator(
        task_id="csv_to_raw",
        python_callable=csv_to_raw
    )

    raw_to_staging_task = PythonOperator(
        task_id="raw_to_staging",
        python_callable=raw_to_staging
    )

    staging_to_curated_task = PythonOperator(
        task_id="staging_to_curated",
        python_callable=staging_to_curated
    )

    validate_task = PythonOperator(
        task_id="validate_pipeline",
        python_callable=validate_pipeline
    )

    csv_to_raw_task >> raw_to_staging_task >> staging_to_curated_task >> validate_task
