from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

from postgres_value_check_operator import PostgresValueCheckOperator

DAG_NAME = 'enriched-dag'

args = {
    'start_date': datetime(2019, 9, 27)
}

dag = DAG(
    DAG_NAME,
    catchup=False,
    default_args=args,
    schedule_interval= '00 08 * * *'
)

with dag as dag:
    finish_transform = DummyOperator(
        task_id='finish_transform'
    )

    create_schema = PostgresOperator(
        task_id='create_schema',
        sql='sql/enriched/create_schema_enriched.sql'
    )

    create_table_drug = PostgresOperator(
        task_id='create_table_drug',
        sql='sql/enriched/tables/create_table_drug_dim.sql'
    )

    create_table_provider = PostgresOperator(
        task_id='create_table_provider',
        sql='sql/enriched/tables/create_table_provider_dim.sql'
    )
    
    check_table_provider = PostgresValueCheckOperator(
        task_id = 'check_table_provider',
        sql = 'sql/enriched/tests/test_table_provider_dim.sql',
        pass_value=True
    )
    
    check_table_drug = PostgresValueCheckOperator(
        task_id = 'check_table_drug',
        sql = 'sql/enriched/tests/test_table_drug_dim.sql',
        pass_value=True
    )

    finish_tests = DummyOperator(
        task_id='finish_tests'
    )
    
    create_schema >> [create_table_drug, create_table_provider] >> finish_transform >> [check_table_provider, check_table_drug] >> finish_tests