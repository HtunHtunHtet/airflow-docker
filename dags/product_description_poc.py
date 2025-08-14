from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Sample DAG showing basic product description pipeline
default_args = {
    'owner': 'htunhtunhtet',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'product_description_poc',
    default_args=default_args,
    description='POC for product description generation',
    schedule_interval=timedelta(days=1),
)

def fetch_product_data():
    # Simulate fetching product data
    return {'product_id': '123', 'name': 'Test Product'}

def generate_description(ti):
    # Get product data from previous task
    product = ti.xcom_pull(task_ids='fetch_product_data')
    return f"Description for {product['name']}"

def save_description(ti):
    # Get generated description
    description = ti.xcom_pull(task_ids='generate_description')
    print(f"Saving: {description}")

# Define tasks
t1 = PythonOperator(
    task_id='fetch_product_data',
    python_callable=fetch_product_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='generate_description',
    python_callable=generate_description,
    dag=dag,
)

t3 = PythonOperator(
    task_id='save_description',
    python_callable=save_description,
    dag=dag,
)

# Set dependencies
t1 >> t2 >> t3