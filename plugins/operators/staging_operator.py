from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StagingOperator(BaseOperator):
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
        self,
        schema,
        table,
        path,
        postgres_conn_id='postgres_default',
        autocommit=False,
        parameters=None,
        *args, **kwargs
    ):
        super(StagingOperator, self).__init__(*args, **kwargs)
        self.schema = schema
        self.table = table
        self.path = path
        self.postgres_conn_id = postgres_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
    
    def execute(self, context):
        self.hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        
        self.log.info('Executing CREATE command')
        self.hook.run(self.get_staging_table_filepath(), self.autocommit)
        self.log.info('Finished CREATE command')

        copy_query = """
        COPY {schema}.{table}
        FROM '{path}'
        DELIMITERS ',' CSV
        """.format(
            schema=self.schema,
            table=self.table,
            path = self.path
        )

        self.log.info('Executing COPY Command')
        self.hook.run(copy_query, self.autocommit)
        self.log.info('Finished Executing COPY command')
    
    def get_staging_table_filepath():
        return 'sql/staging/tables/create_table_' + self.table + '.sql'