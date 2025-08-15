from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.time_delta import TimeDeltaSensor
from airflow.sensors.base import BaseSensorOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import random

# Custom Sensor for Product Availability
class ProductAvailabilitySensor(BaseSensorOperator):
    """
    Custom sensor that waits for product to be available for processing
    """

    def __init__(self, product_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id = product_id

    def poke(self, context):
    
        # Simulate checking product availability (random for demo)
        available = random.choice([True, False, False])  # 33% chance

        if available:
            self.log.info(f"Product {self.product_id} is available for processing!")
            return True
        else:
            self.log.info(f"Product {self.product_id} not ready yet, waiting...")
            return False

# DAG Definition
default_args = {
    'owner': 'htunhtunhtet',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'sensors_demo',
    default_args=default_args,
    description='Demo of different sensor types',
    schedule_interval=None,
    catchup=False,
    tags=['sensors', 'advanced'],
)

# Functions for processing
def create_test_file():
    """Create a test file for FileSensor to detect"""
    file_path = '/tmp/product_data_ready.txt'
    with open(file_path, 'w') as f:
        f.write('Product data is ready for processing')
    print(f"Created file: {file_path}")

def process_product():
    """Simulate product processing"""
    print("Processing product after all sensors passed!")
    return "Product processed successfully"

# Tasks
create_file_task = PythonOperator(
    task_id='create_test_file',
    python_callable=create_test_file,
    dag=dag,
)

# Sensor 1: Wait for file to exist
file_sensor = FileSensor(
    task_id='wait_for_product_file',
    filepath='/tmp/product_data_ready.txt',
    poke_interval=10,  # Check every 10 seconds
    timeout=300,       # Give up after 5 minutes
    dag=dag,
)

# Sensor 2: Wait for time period
time_sensor = TimeDeltaSensor(
    task_id='wait_for_processing_window',
    delta=timedelta(seconds=30),  # Wait 30 seconds
    dag=dag,
)

# Sensor 3: Custom product availability sensor
product_sensor = ProductAvailabilitySensor(
    task_id='wait_for_product_availability',
    product_id='PROD-001',
    poke_interval=5,   # Check every 5 seconds
    timeout=120,       # Give up after 2 minutes
    dag=dag,
)

# Final processing task
process_task = PythonOperator(
    task_id='process_product',
    python_callable=process_product,
    dag=dag,
)

# Dependencies
create_file_task >> file_sensor >> time_sensor >> product_sensor >> process_task