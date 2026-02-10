CREATE TABLE etl_dag_runs (
    run_id        VARCHAR(50) PRIMARY KEY,
    dag_name      VARCHAR(100),
    start_time    TIMESTAMP,
    end_time      TIMESTAMP,
    status        VARCHAR(20)
);

CREATE TABLE etl_step_runs (
    step_id       INT AUTO_INCREMENT PRIMARY KEY,
    run_id        VARCHAR(50),
    step_name     VARCHAR(100),
    start_time    TIMESTAMP,
    end_time      TIMESTAMP,
    status        VARCHAR(20),
    records_processed INT,
    error_message TEXT,
    FOREIGN KEY (run_id) REFERENCES etl_dag_runs(run_id)
);

CREATE TABLE etl_pipeline_history (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    dag_name      VARCHAR(100),
    run_date      DATE,
    status        VARCHAR(20),
    total_records INT
);

CREATE TABLE etl_metrics (
    metric_id     INT AUTO_INCREMENT PRIMARY KEY,
    run_id        VARCHAR(50),
    metric_name   VARCHAR(100),
    metric_value  FLOAT,
    recorded_at   TIMESTAMP
);
