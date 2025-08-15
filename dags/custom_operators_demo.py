from airflow import DAG
from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from datetime import datetime, timedelta
import logging

# Custom Operator Definition
class ProductProcessorOperator(BaseOperator):
    """
    Custom operator for processing product data
    """

    @apply_defaults
    def __init__(self, product_id, processing_type='description', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product_id = product_id
        self.processing_type = processing_type

    def execute(self, context):
        """
        Main execution logic
        """
        logging.info(f"Processing product {self.product_id} for {self.processing_type}")

        # Simulate product processing
        if self.processing_type == 'description':
            result = f"Generated description for product {self.product_id}"
        elif self.processing_type == 'validation':
            result = f"Validated product {self.product_id}"
        else:
            result = f"Processed product {self.product_id}"

        logging.info(f"Result: {result}")
        return result

# DAG Definition
default_args = {
    'owner': 'htunhtunhtet',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'custom_operators_demo',
    default_args=default_args,
    description='Demo of custom operators',
    schedule_interval=None,
    catchup=False,
    tags=['custom-operators', 'advanced'],
)

# Using the Custom Operator
process_product_1 = ProductProcessorOperator(
    task_id='process_product_1',
    product_id='PROD-001',
    processing_type='description',
    dag=dag,
)

validate_product_1 = ProductProcessorOperator(
    task_id='validate_product_1',
    product_id='PROD-001',
    processing_type='validation',
    dag=dag,
)

# Set dependencies
process_product_1 >> validate_product_1