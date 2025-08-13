from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args= {
    'owner': 'htunhtunhtet',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
}

dag = DAG(
    "traditional_operators",
    default_args= default_args,
    description= "A traditional operator DAG",
    schedule_interval=None,
    catchup=False,
    tags=["operators"]
)

def generate_data(**context):
    import random

    data = {
        'timestamp': str(datetime.now()),
        'random_number': random.randint(1, 100),
        'message': 'Hello from the pyton tasks'
    }

    print(f"Generated data: {data}")

    context['task_instance'].xcom_push(key='generated_data', value=data)
    
    return data

def process_bash_result(**context):
    ## pull form xcom
    bash_result = context['task_instance'].xcom_pull(task_ids='bash_task')
    original_data = context['task_instance'].xcom_pull(key='generated_data', task_ids='python_generate')

    print(f"Bash task returned: {bash_result}")
    print(f"Original data was: {original_data}")

    final_result = f"Proceed: {bash_result} | Original number: {original_data['random_number']}"
    print(f"Final result: {final_result}")

    return final_result


python_generate = PythonOperator(
    task_id='python_generate',
    python_callable=generate_data,
    dag=dag,
)

bash_task = BashOperator(
    task_id='bash_task',
    bash_command='''
    echo "Bash task started"
    echo "Current date: $(date)"
    echo "Processing data from Python task"
    echo "Bash processing complete"
    ''',
    dag=dag,
)

python_process = PythonOperator(
    task_id='python_process',
    python_callable=process_bash_result,
    dag=dag,
)

python_generate >> bash_task >> python_process