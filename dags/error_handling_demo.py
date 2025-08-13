from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import random

default_args = {
    'owner': 'htunhtunhtet',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 2,  # Default retries for all tasks
    'retry_delay': timedelta(minutes=1),  # Wait 1 min between retries
    'email_on_failure': False,
    'email_on_retry': False,
}

dag = DAG(
    'error_handling_demo',
    default_args=default_args,
    description='Error handling and retries',
    schedule_interval=None,
    catchup=False,
    tags=['error-handling', 'retries']
)

def always_succeeds(**context):
    """This task always succeeds"""
    print("This task always works!")

def sometimes_fails(**context):
    """This task fails 70% of the time"""
    if random.random() < 0.7:
        print("Task failed! Will retry...")
        raise Exception("Random Failure occured!")
    
    print ("Task succeed after retires !")
    return "finally succeed"

def always_fails(**context):
    """This task always fails"""
    raise Exception("This task always fails!")

def cleanup_task(**context):
    print("Cleanup task running...")
    return "cleanup_complete"

# Creating Operators with different retry settings

# Always succeeds 
success_task = PythonOperator(
    task_id='always_succeeds',
    python_callable=always_succeeds,
    dag=dag
)

# Sometime fails
unreliable_task = PythonOperator(
    task_id='somtimes_fails',
    python_callable=sometimes_fails,
    retries=3,
    retry_delay=timedelta(seconds=30),
    dag=dag
)

# Always fails
always_fails = PythonOperator(
    task_id='always_fails',
    python_callable=always_fails,
    retries=1,
    retry_delay=timedelta(seconds=30),
    dag=dag
)

# Cleanup Task
cleanup = PythonOperator(
    task_id='cleanup_task',
    python_callable=cleanup_task,
    retries=0,
    trigger_rule='all_done',
    dag=dag
)

# Dependencies
success_task >> [unreliable_task, always_fails] >> cleanup
