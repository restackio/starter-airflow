from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook

def retrieve_data(**kwargs):
    hook = PostgresHook(postgres_conn_id='your_postgres_connection_id')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM public."Company" LIMIT 5')  # Using single quotes for the SQL query
    rows = cursor.fetchall()
    
    # Push results to XCom
    task_instance = kwargs['ti']
    task_instance.xcom_push(key='query_results', value=rows)
    
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
          schedule_interval=None,  # Manually triggered
          )

t1 = PythonOperator(
    task_id='retrieve_data',
    python_callable=retrieve_data,
    dag=dag,
    provide_context=True,  # Required to get the task_instance (ti) variable
)

t1
