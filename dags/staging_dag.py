from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

from staging_operator import (StagingOperator)
from postgres_value_check_operator import PostgresValueCheckOperator

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
    finish_staging = DummyOperator(
        task_id='finish_staging'
    )

    create_schema = PostgresOperator(
        task_id='create_schema',
        sql='sql/staging/create_schema_staging.sql'
    )

    load_ownership = StagingOperator(
        task_id='load_ownership',
        sql='sql/staging/tables/create_table_ownership.sql',
        schema='staging',
        table='ownership',
        path='/home/data/PGYR17_P062819/OP_DTL_OWNRSHP_PGYR2017_P06282019.csv',
        copy_options="DELIMITER ',' CSV HEADER"
    )

    load_npi_drug = StagingOperator(
        task_id='load_npi_drug',
        sql='sql/staging/tables/create_table_npi_drug.sql',
        schema='staging',
        table='npi_drug',
        path='/home/data/PartD_Prescriber_PUF_NPI_DRUG_17/PartD_Prescriber_PUF_NPI_Drug_17.txt',
        copy_options='HEADER'
    )


    load_payments = StagingOperator(
        task_id='load_payments',
        sql='sql/staging/tables/create_table_payments.sql',
        schema='staging',
        table='payments',
        path='/home/data/PGYR17_P062819/OP_DTL_GNRL_PGYR2017_P06282019.csv',
        copy_options="DELIMITER ',' CSV HEADER"
    )
    
    check_ownership = PostgresValueCheckOperator(
        task_id = 'check_ownership',
        sql = 'sql/staging/tests/test_table_ownership.sql',
        pass_value=True
    )

    check_npi_drug = PostgresValueCheckOperator(
        task_id = 'check_npi_drug',
        sql = 'sql/staging/tests/test_table_npi_drug.sql',
        pass_value=True
    )

    check_payments = PostgresValueCheckOperator(
        task_id = 'check_payments',
        sql = 'sql/staging/tests/test_table_payments.sql',
        pass_value=True
    )

    finish_tests = DummyOperator(
        task_id='finish_tests'
    )
    
    create_schema >> [load_ownership, load_npi_drug, load_payments] >> finish_staging >> [check_ownership, check_npi_drug, check_payments] >> finish_tests