from fastapi import FastAPI
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# -----------------------------------
# ENABLE CORS (IMPORTANT)
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# AIRFLOW CONFIG
# -----------------------------------
AIRFLOW_URL = "http://localhost:8081/api/v1"

USERNAME = "airflow"
PASSWORD = "airflow"


# -----------------------------------
# HEALTH CHECK
# -----------------------------------
@app.get("/")
def home():
    return {"message": "Backend is running"}


# -----------------------------------
# GET ALL DAGS
# -----------------------------------
@app.get("/dags")
def get_dags():

    res = requests.get(
        f"{AIRFLOW_URL}/dags",
        auth=(USERNAME, PASSWORD)
    )

    return res.json()


# -----------------------------------
# GET DAG RUNS
# -----------------------------------
@app.get("/dag-runs/{dag_id}")
def get_dag_runs(dag_id: str):

    res = requests.get(
        f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns",
        auth=(USERNAME, PASSWORD)
    )

    return res.json()
@app.get("/stats")
def get_stats():

    # Get all DAGs
    dags_res = requests.get(
        f"{AIRFLOW_URL}/dags",
        auth=(USERNAME, PASSWORD)
    ).json()

    dags = dags_res.get("dags", [])

    total_dags = len(dags)

    active_dags = len([d for d in dags if not d["is_paused"]])

    # Get running dag runs
    runs_res = requests.get(
        f"{AIRFLOW_URL}/dagRuns",
        auth=(USERNAME, PASSWORD)
    ).json()

    runs = runs_res.get("dag_runs", [])

    running = len([r for r in runs if r["state"] == "running"])

    success = len([r for r in runs if r["state"] == "success"])

    total_runs = len(runs)

    success_rate = (
        round((success / total_runs) * 100, 2)
        if total_runs > 0 else 0
    )

    return {
        "total_dags": total_dags,
        "active_dags": active_dags,
        "running": running,
        "success_rate": success_rate
    }
