from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

from staging_operator import (StagingOperator)

DAG_NAME = 'staging-dag'

args = {
    'start_date': datetime(2019, 9, 27)
}

dag = DAG(
    DAG_NAME,
    catchup=False,
    default_args=args,
    schedule_interval= '00 00 * * *'
)

with dag as dag:
    finish = DummyOperator(
        task_id='finish_staging'
    )

    load_ownership = StagingOperator(
        task_id='load_ownership',
        sql='sql/staging/tables/create_table_ownership.sql',
        schema='fraud',
        table='ownership',
        path='/home/data/PGYR17_P062819/OP_DTL_OWNRSHP_PGYR2017_P06282019.csv'
    )

    finish >> load_ownership