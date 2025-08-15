from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Configuration for different product categories
PRODUCT_CATEGORIES = {
    'electronics': {
        'processing_time': 30,
        'validation_rules': ['price_check', 'warranty_info'],
        'schedule': '@daily'
    },
    'clothing': {
        'processing_time': 15,
        'validation_rules': ['size_chart', 'material_info'],
        'schedule': '@hourly'
    },
    'books': {
        'processing_time': 10,
        'validation_rules': ['isbn_check', 'author_info'],
        'schedule': None  # Manual only
    }
}

def create_product_processing_dag(category, config):
    """
    Factory function to create a DAG for a specific product category
    """

    # Dynamic DAG configuration
    dag_id = f'product_pipeline_{category}'

    default_args = {
        'owner': 'htunhtunhtet',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    # Create the DAG
    dag = DAG(
        dag_id,
        default_args=default_args,
        description=f'Product processing pipeline for {category}',
        schedule_interval=config['schedule'],
        catchup=False,
        tags=['dynamic', 'product-pipeline', category],
    )

    # Dynamic task functions
    def fetch_products(**context):
        category = context['dag'].dag_id.split('_')[-1]
        print(f"Fetching {category} products...")
        return f"Found 10 {category} products"

    def process_products(**context):
        category = context['dag'].dag_id.split('_')[-1]
        processing_time = PRODUCT_CATEGORIES[category]['processing_time']
        print(f"Processing {category} products (estimated {processing_time}s each)...")
        return f"Processed {category} products"

    def validate_products(**context):
        category = context['dag'].dag_id.split('_')[-1]
        rules = PRODUCT_CATEGORIES[category]['validation_rules']
        print(f"Validating {category} products with rules: {rules}")
        return f"Validated {category} products"

    def save_results(**context):
        category = context['dag'].dag_id.split('_')[-1]
        print(f"Saving {category} product results...")
        return f"Saved {category} results"

    # Create tasks dynamically
    fetch_task = PythonOperator(
        task_id='fetch_products',
        python_callable=fetch_products,
        dag=dag,
    )

    process_task = PythonOperator(
        task_id='process_products',
        python_callable=process_products,
        dag=dag,
    )

    validate_task = PythonOperator(
        task_id='validate_products',
        python_callable=validate_products,
        dag=dag,
    )

    save_task = PythonOperator(
        task_id='save_results',
        python_callable=save_results,
        dag=dag,
    )

    # Set dependencies
    fetch_task >> process_task >> validate_task >> save_task

    return dag

# Generate DAGs dynamically
for category, config in PRODUCT_CATEGORIES.items():
    # Create a DAG for each product category
    dag_id = f'product_pipeline_{category}'
    globals()[dag_id] = create_product_processing_dag(category, config)