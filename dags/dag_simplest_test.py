"""A simple Hello World DAG"""
from datetime import datetime, timedelta

from airflow.decorators import dag, task

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 12, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


@dag(
    default_args=default_args,
    doc_md=__doc__,
    schedule=timedelta(days=1),
    catchup=False,
)
def hello_world_dag():
    """Hello world DAG"""

    @task
    def hello_world():
        """Print hello world"""
        print("Hello World")


hello_world_dag()
