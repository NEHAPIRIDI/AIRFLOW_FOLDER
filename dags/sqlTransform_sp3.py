import sys
import os
sys.path.append("/opt/airflow/scripts")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Python ETL tasks
from csv_to_raw import csv_to_raw
from raw_to_staging import raw_to_staging
from validate_pipeline import validate_pipeline

# SQL-based transformation runner
from run_sql import run_sql_file

default_args = {
    "owner": "admin",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="amazon_etl_pipeline_sql",
    description="Amazon CSV ETL Pipeline (RAW → STAGING → CURATED)",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["amazon", "etl"],
) as dag:

    # 1️⃣ CSV → RAW
    csv_to_raw_task = PythonOperator(
        task_id="csv_to_raw",
        python_callable=csv_to_raw
    )

    # 2️⃣ RAW → STAGING
    raw_to_staging_task = PythonOperator(
        task_id="raw_to_staging",
        python_callable=raw_to_staging
    )

    # 3️⃣ STAGING → CURATED (SQL CTE TRANSFORMATION)
    sql_transform_task = PythonOperator(
        task_id="sql_staging_to_curated",
        python_callable=run_sql_file,
        op_args=["/opt/airflow/data_models/sql/stg_to_curated.sql"]
    )

    # 4️⃣ VALIDATION
    validate_task = PythonOperator(
        task_id="validate_pipeline",
        python_callable=validate_pipeline
    )

    # DAG ORDER
    csv_to_raw_task >> raw_to_staging_task >> sql_transform_task >> validate_task
