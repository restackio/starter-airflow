"""
A basic dbt DAG that shows how to run dbt commands via the BashOperator

Follows the standard dbt seed, run, and test pattern.
"""
import os
from pathlib import Path
from pendulum import datetime

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.decorators import dag, task

# We're hardcoding this value here for the purpose of the demo, but in a production environment this
# would probably come from a config file and/or environment variables!
DBT_PROJECT_DIR = os.environ["DBT_PROJECT_DIR"]


@dag("dbt_basic_dag",
    start_date=datetime(2020, 12, 23),
    description="A sample Airflow DAG to invoke dbt runs using a BashOperator",
    schedule=None,
    catchup=False)
def dbt_dag():

    # This task loads the CSV files from dbt/data into the local postgres database for the purpose of this demo.
    # In practice, we'd usually expect the data to have already been loaded to the database.

    # Seed is not having support at the moment
    #dbt_seed = BashOperator(
    #    task_id="dbt_seed",
    #    bash_command=f"cd {DBT_PROJECT_DIR} && dbt seed --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    #)

    @task
    def prepare_data():
        from google.cloud import storage

        client = storage.Client()
        bucket = client.get_bucket(os.environ['GCS_BUCKET_NAME'])
        files = Path(DBT_PROJECT_DIR).glob('seeds/*.csv')
        for file in files:
            filename = str(file).split('/')[-1]
            blob = bucket.blob(f'data/{filename}')
            blob.upload_from_filename(file)

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt run --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    # TODO: Going to iterate DBT test in a new PR.
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT_DIR} && dbt test --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    #dbt_seed >> dbt_run >> dbt_test
    prepare_data() >> dbt_run >> dbt_test

dbt_dag()
