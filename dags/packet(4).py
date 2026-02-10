from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

INPUT_FILE = "/opt/airflow/data/raw/Amazon.csv"
STAGING_OUTPUT = "/opt/airflow/data/raw/st_op.csv"
CURATED_OUTPUT = "/opt/airflow/data/raw/cr_op.csv"

def streaming_etl():
    chunk_size = 10000
    first_chunk_st = True
    first_chunk_cr = True
    chunk_no = 1

    for chunk in pd.read_csv(INPUT_FILE, chunksize=chunk_size):

        # -----------------------------
        # STAGING: Remove NULL rows
        # -----------------------------
        staging_df = chunk.dropna()

        staging_df.to_csv(
            STAGING_OUTPUT,
            mode="a",
            index=False,
            header=first_chunk_st
        )
        first_chunk_st = False

        # -----------------------------
        # CURATED: Add derived column
        # -----------------------------
        curated_df = staging_df.copy()
        curated_df["total_amount"] = (
            curated_df["UnitPrice"] * curated_df["Quantity"]
        )

        curated_df.to_csv(
            CURATED_OUTPUT,
            mode="a",
            index=False,
            header=first_chunk_cr
        )
        first_chunk_cr = False

        print(f"✅ Chunk {chunk_no} read and processed successfully")

        chunk_no += 1


with DAG(
    dag_id="streaming_batch_etl",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    etl_task = PythonOperator(
        task_id="streaming_processing",
        python_callable=streaming_etl
    )
