"""Test DAG"""
from airflow.models.dag import DAG
from airflow.operators.empty import EmptyOperator
import pendulum

with DAG(
    "test_dag_v1",
    schedule="*/10 * * * *",
    default_args={"depends_on_past": True},
    doc_md=__doc__,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
):

    run_this_1 = EmptyOperator(task_id="run_this_1")
    run_this_2 = EmptyOperator(task_id="run_this_2")
    run_this_3 = EmptyOperator(task_id="run_this_3")

    run_this_1 >> run_this_2 >> run_this_3  # pylint: disable=W0104
