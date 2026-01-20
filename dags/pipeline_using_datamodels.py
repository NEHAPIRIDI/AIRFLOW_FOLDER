import sys
sys.path.append("/opt/airflow/scripts")


from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Import ETL functions
from apply_data_models import apply_data_models
from csv_to_raw import csv_to_raw
from raw_to_staging import raw_to_staging
from staging_to_curated import staging_to_curated
from validate_pipeline import validate_pipeline


# -----------------------------
# DEFAULT ARGS
# -----------------------------
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


# -----------------------------
# DAG DEFINITION
# -----------------------------
with DAG(
    dag_id="amazon_etl_pipeline_datamodels",
    description="Amazon CSV → Raw → Staging → Curated ETL using Data Models",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,     # manual trigger
    catchup=False,
    tags=["amazon", "etl", "mysql"],
) as dag:

    # -----------------------------
    # TASK 1: APPLY DATA MODELS
    # -----------------------------
    apply_models = PythonOperator(
        task_id="apply_data_models",
        python_callable=apply_data_models
    )

    # -----------------------------
    # TASK 2: CSV → RAW
    # -----------------------------
    load_raw = PythonOperator(
        task_id="csv_to_raw",
        python_callable=csv_to_raw
    )

    # -----------------------------
    # TASK 3: RAW → STAGING
    # -----------------------------
    load_staging = PythonOperator(
        task_id="raw_to_staging",
        python_callable=raw_to_staging
    )

    # -----------------------------
    # TASK 4: STAGING → CURATED
    # -----------------------------
    load_curated = PythonOperator(
        task_id="staging_to_curated",
        python_callable=staging_to_curated
    )

    # -----------------------------
    # TASK 5: VALIDATION
    # -----------------------------
    validate = PythonOperator(
        task_id="validate_pipeline",
        python_callable=validate_pipeline
    )

    # -----------------------------
    # TASK DEPENDENCIES
    # -----------------------------
    apply_models >> load_raw >> load_staging >> load_curated >> validate
