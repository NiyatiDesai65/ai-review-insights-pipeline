# dags/amazon_review_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, '/usr/local/airflow')

from src.ingestion.kaggle_reader import ingest
from src.processing.cleaner import clean
from src.ai.analyzer import analyse
from src.reporting.reporter import run
from src.logger import get_logger

logger = get_logger("dag")

# ---- default settings ----
default_args = {
    'owner': 'niyati',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# ---- define DAG ----
dag = DAG(
    'amazon_review_pipeline',
    default_args=default_args,
    description='AI powered Amazon review analysis pipeline',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False
)

# ---- task functions ----
def task_ingest(**context):
    logger.info("Task 1 started — ingestion")
    reviews = ingest()
    # push to XCom so next task can use it
    context['ti'].xcom_push(key='reviews', value=reviews)
    logger.info(f"Task 1 complete — {len(reviews)} reviews ingested")

def task_clean(**context):
    logger.info("Task 2 started — cleaning")
    # pull reviews from previous task
    reviews = context['ti'].xcom_pull(key='reviews', task_ids='ingest')
    cleaned = clean(reviews)
    context['ti'].xcom_push(key='cleaned_reviews', value=cleaned)
    logger.info(f"Task 2 complete — {len(cleaned)} reviews cleaned")

def task_analyse(**context):
    logger.info("Task 3 started — AI analysis")
    cleaned = context['ti'].xcom_pull(key='cleaned_reviews', task_ids='clean')
    results = analyse(cleaned)
    context['ti'].xcom_push(key='results', value=results)
    logger.info(f"Task 3 complete — {len(results)} reviews analysed")

def task_report(**context):
    logger.info("Task 4 started — reporting")
    results = context['ti'].xcom_pull(key='results', task_ids='analyse')
    run(results)
    logger.info("Task 4 complete — report generated")

# ---- define tasks ----
ingest_task = PythonOperator(
    task_id='ingest',
    python_callable=task_ingest,
    dag=dag
)

clean_task = PythonOperator(
    task_id='clean',
    python_callable=task_clean,
    dag=dag
)

analyse_task = PythonOperator(
    task_id='analyse',
    python_callable=task_analyse,
    dag=dag
)

report_task = PythonOperator(
    task_id='report',
    python_callable=task_report,
    dag=dag
)

# ---- set task order ----
ingest_task >> clean_task >> analyse_task >> report_task