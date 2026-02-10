from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


AIRFLOW_URL = "http://localhost:8081/api/v1"
USERNAME = "airflow"
PASSWORD = "airflow"


def airflow_get(endpoint):
    r = requests.get(
        f"{AIRFLOW_URL}{endpoint}",
        auth=(USERNAME, PASSWORD)
    )
    return r.json()


@app.route("/api/health")
def health():
    data = airflow_get("/health")
    return jsonify({"success": True, "data": data})


@app.route("/api/dags")
def dags():
    data = airflow_get("/dags")
    return jsonify({"success": True, "data": data["dags"]})


@app.route("/api/dags/<dag_id>/runs")
def dag_runs(dag_id):
    data = airflow_get(f"/dags/{dag_id}/dagRuns")
    return jsonify({"success": True, "data": data})


@app.route("/api/dags/<dag_id>/tasks")
def dag_tasks(dag_id):
    data = airflow_get(f"/dags/{dag_id}/tasks")
    return jsonify({"success": True, "data": data})


@app.route("/api/dags/<dag_id>/status")
def dag_status(dag_id):
    data = airflow_get(f"/dags/{dag_id}/dagRuns?limit=1")

    latest_run = None
    if "dag_runs" in data and len(data["dag_runs"]) > 0:
        latest_run = data["dag_runs"][0]

    return jsonify({
        "success": True,
        "dag_id": dag_id,
        "latest_run": latest_run
    })


if __name__ == "__main__":
    app.run(port=5000, debug=True)
