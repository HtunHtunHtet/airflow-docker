import json
import pendulum

from airflow.decorators import dag, task
from airflow.utils.task_group import TaskGroup

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"]
)
def task_groups_example():
    