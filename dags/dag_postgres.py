from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

def retrieve_data():
    hook = PostgresHook(postgres_conn_id='your_postgres_connection_id')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Public.Company LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 18),
    'retries': 1,
}

dag = DAG('simple_postgres_dag',
          default_args=default_args,
          description='A simple DAG to retrieve data from PostgreSQL',
          schedule_interval=None,
          )

t1 = PythonOperator(
    task_id='retrieve_data',
    python_callable=retrieve_data,
    dag=dag,
)

t1
