from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import mysql.connector

from scd1_mapping_wrapper import scd1_mapping


def run_category_scd1_mapping():
    conn = mysql.connector.connect(
        host="mysql",
        user="airflow_user",
        password="airflow_pass",
        database="amazon_db"
    )

    scd1_mapping(
        conn=conn,
        source_table="ref_category_source",
        target_table="ref_category",
        key_columns=["source_category"],
        update_columns=["standard_category"]
    )

    conn.close()
    print("✅ SCD-1 Category reference mapping completed")


with DAG(
    dag_id="scd1_reference_mapping",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["scd1", "reference", "etl"],
) as dag:

    scd1_category_mapping = PythonOperator(
        task_id="scd1_category_mapping",
        python_callable=run_category_scd1_mapping
    )
