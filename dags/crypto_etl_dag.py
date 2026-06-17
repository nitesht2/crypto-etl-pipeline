"""Airflow DAG: run the crypto ETL daily as extract -> transform -> load.

Drop this file in your Airflow `dags/` folder. It calls the same functions the
CLI scripts use, so there is one source of truth for the pipeline logic.
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from extract import extract_top_coins
from transform import transform_data
from load import load_data

default_args = {
    "owner": "data-eng",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def _extract() -> None:
    extract_top_coins().to_csv("top_coins.csv", index=False)


with DAG(
    dag_id="crypto_etl",
    description="Daily CoinGecko -> PostgreSQL fact_coin_price load",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["crypto", "etl"],
) as dag:
    extract = PythonOperator(task_id="extract", python_callable=_extract)
    transform = PythonOperator(task_id="transform", python_callable=transform_data)
    load = PythonOperator(task_id="load", python_callable=load_data)

    extract >> transform >> load
