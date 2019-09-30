from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.plugins_manager import AirflowPlugin

class StagingOperator(BaseOperator):
    template_fields = ('sql',)
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(
        self,
        sql,
        schema,
        table,
        path,
        postgres_conn_id='postgres_default',
        copy_options='',
        autocommit=False,
        parameters=None,
        *args, **kwargs
    ):
        super(StagingOperator, self).__init__(*args, **kwargs)
        self.schema = schema
        self.sql = sql
        self.table = table
        self.path = path
        self.postgres_conn_id = postgres_conn_id
        self.copy_options = copy_options
        self.autocommit = autocommit
        self.parameters = parameters
    
    def execute(self, context):
        self.hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)

        self.log.info('Executing CREATE command')
        self.hook.run(self.sql, self.autocommit)
        self.log.info('Finished CREATE command')

        copy_query = """
        COPY {schema}.{table}
        FROM '{path}'
        {copy_options}
        """.format(
            schema=self.schema,
            table=self.table,
            path = self.path,
            copy_options = self.copy_options.upper()
        )

        self.log.info('Executing COPY Command')
        self.hook.run(copy_query, self.autocommit)
        self.log.info('Finished Executing COPY command')

