from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.email import send_email
import pendulum
import csv

CSV_PATH = "/opt/airflow/data/friends_emails.csv"

# Define local timezone (IST)
local_tz = pendulum.timezone("Asia/Kolkata")


def send_christmas_wishes_from_csv():
    recipients = []

    # READ EMAILS FROM CSV
    with open(CSV_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipients.append(row["email"])

    if not recipients:
        print("⚠️ No email addresses found in CSV")
        return

    subject = "🎄 Merry Christmas!"
    html_content = """
    <h2>🎅 Merry Christmas!</h2>
    <p>Wishing you joy, peace, and happiness this Christmas 🎁</p>
    <b>– Sent automatically using Apache Airflow ❄️</b>
    """

    # SEND EMAIL (Outlook SMTP configured in docker-compose)
    send_email(
        to=recipients,
        subject=subject,
        html_content=html_content
    )

    print(f"✅ Christmas wishes sent successfully to {len(recipients)} friends")
    for email in recipients:
        print(f"🎄 Wish sent to: {email}")


# -----------------------------
# DAG DEFINITION (CORRECT)
# -----------------------------
with DAG(
    dag_id="christmas_wishes_dag",
    description="Send Christmas wishes automatically using CSV 🎄",
    start_date=pendulum.datetime(2025, 12, 22, 15, 22, tz=local_tz),  # 5 mins before
    schedule_interval="22 15 20 12 *",  # 🎯 Dec 20 at 3:15 PM
    catchup=False,
    tags=["festival", "email", "automation"],
) as dag:

    send_wishes = PythonOperator(
        task_id="send_christmas_wishes",
        python_callable=send_christmas_wishes_from_csv
    )
