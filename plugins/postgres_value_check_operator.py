from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.check_operator import ValueCheckOperator

class PostgresValueCheckOperator(ValueCheckOperator):
    """
    Performs a simple value check using sql code.

    :param str task_id: a unique, meaningful id for the task (inhereted)
    :param str sql: the sql to be executed. (templated)
        Can receive a str representing a sql statement,
        a list of str (sql statements), or reference to a template file.
        Template reference are recognized by str ending in '.sql'
    :param datetime.timedelta execution_timeout: max time allowed for the execution of
        this task instance, if it goes beyond it will raise and fail (inhereted)
    :param str postgres_conn_id: reference to specific Postgres connection id
    :param any pass_value: Result value for which check will succeed
    :param any tolerance: Tolerance level to pass the test; 0.01 is 1%
    """

    template_fields = ('sql', 'pass_value',)
    template_ext = ('.sql',)
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self,
                 sql,
                 pass_value,
                 tolerance = None,
                 postgres_conn_id = 'postgres_default',
                 parameters=None,
                 autocommit=True,
                 warehouse=None,
                 database=None,
                 role=None,
                 schema=None,
                 *args, **kwargs) -> None:

        super().__init__(sql=sql, pass_value=pass_value, tolerance=tolerance,
                         *args, **kwargs)

        self.postgres_conn_id = postgres_conn_id
        self.sql = sql
        self.autocommit = autocommit

    def get_db_hook(self):
        return PostgresHook(postgres_conn_id=self.postgres_conn_id)
