import json
from typing import List

import pendulum

from airflow.decorators import dag, task

# from airflow.sdk import dag, task
@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def dynamic_tasks():
    @task()
    def get_items()-> List[str]:
        return ["NYC", "LA", "Chicago"]
    
    @task()
    def process_item(item:str)-> dict:
        import random
        temp = random.randint(60,90)
        return {"city": item, "temperature": temp}
    
    # Dynamic generation
    items = get_items()
    results = process_item.expand(item=items)

dynamic_tasks()