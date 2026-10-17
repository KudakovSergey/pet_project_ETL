from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from etl.extract import extract_all
from etl.load import get_connection, create_tables, insert_weather
from etl.transform import build_daily_summary

default_args = {
    "owner": "sergey",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "start_date": datetime(2026, 10, 1),
}

def task_extract(**kwargs):
    data = extract_all()
    return data

def task_load(**kwargs):
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='task_extract')

    conn = get_connection()
    try:
        create_tables(conn)
        insert_weather(conn, data)
    finally:
        conn.close()

def task_transform(**kwargs):
    conn = get_connection()
    try:
        build_daily_summary(conn)
    finally:
        conn.close()

with DAG(
    dag_id='weather_elt_pipeline',
    default_args=default_args,
    description='ELT пайплайн для данных о погоде',
    schedule = "@hourly",
    catchup=False,
    tags=["weather" ,"elt"]
) as dag:

    t1_extract = PythonOperator(
        task_id='task_extract',
        python_callable=task_extract,
    )

    t2_load = PythonOperator(
        task_id='task_load',
        python_callable=task_load,
    )

    t3_transform = PythonOperator(
        task_id='task_transform',
        python_callable=task_transform,
    )

t1_extract >> t2_load >> t3_transform
