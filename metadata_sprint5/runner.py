# runner.py
import uuid
import json
import pandas as pd

from data_pipeline_sprint4.fetch_api import fetch_data
from data_pipeline_sprint4.clean import clean_data
from data_pipeline_sprint4.transform import transform_data

from logger import log_dag_start, log_dag_end
from step_logger import log_step_start, log_step_end


def main():
    run_id = str(uuid.uuid4())
    dag_name = "api_etl_metadata_pipeline"

    log_dag_start(run_id, dag_name)

    try:
        # EXTRACT
        log_step_start(run_id, "extract")
        data = fetch_data()
        log_step_end(run_id, "extract", "SUCCESS", len(data))

        # STAGING
        with open("raw_api_data.json", "w") as f:
            json.dump(data, f)

        df = pd.DataFrame(data)

        # CLEAN
        log_step_start(run_id, "clean")
        df = clean_data(df)
        log_step_end(run_id, "clean", "SUCCESS", len(df))

        # TRANSFORM
        log_step_start(run_id, "transform")
        df = transform_data(df)
        log_step_end(run_id, "transform", "SUCCESS", len(df))

        log_dag_end(run_id, "SUCCESS")

    except Exception as e:
        log_dag_end(run_id, "FAILED")
        raise


if __name__ == "__main__":
    main()
