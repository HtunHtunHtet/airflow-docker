from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pendulum

# Daily Schedule
def daily_task_function(**context):
    print(f"Daily task running at: {datetime.now()}")
    print(f"Execution date: {context['ds']}")  # ds = date string
    return "daily_complete"

daily_dag = DAG(
    'daily_schedule',
    default_args={
        'owner': 'htunhtunhtet',
        'depends_on_past': False,
        'start_date': pendulum.datetime(2024, 1, 1, tz="UTC"),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Daily scheduling',
    schedule_interval='@daily',  # Traditional parameter name
    catchup=False,
    tags=['scheduling', 'daily'],
)

daily_task = PythonOperator(
    task_id='daily_task',
    python_callable=daily_task_function,
    dag=daily_dag,
)

#  Hourly Schedule
def hourly_task_function(**context):
    print(f"Hourly task running at: {datetime.now()}")
    print(f"Execution date: {context['ds']}")  # ds = date string
    return "hourly_complete"

hourly_dag = DAG(
    'hourly_schedule_demo',
    default_args={
        'owner': 'htunhtunhtet',
        'depends_on_past': False,
        'start_date': pendulum.datetime(2024, 1, 1, tz="UTC"),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Hourly scheduling demo',
    schedule_interval='@hourly',  # Runs every hour
    catchup=False,
    tags=['scheduling', 'hourly'],
)

hourly_task = PythonOperator(
    task_id='hourly_task',
    python_callable=hourly_task_function,
    dag=hourly_dag,
)

# Custom Cron Schedule (Every weekday at 9 AM)
def weekday_task_function(**context):
    print(f"Weekday task running at: {datetime.now()}")
    print(f"This runs Monday-Friday at 9 AM")
    return "weekday_complete"

weekday_dag = DAG(
    'weekday_schedule_demo',
    default_args={
        'owner': 'htunhtunhtet',
        'depends_on_past': False,
        'start_date': pendulum.datetime(2024, 1, 1, tz="UTC"),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Weekday 9 AM scheduling demo',
    schedule_interval='0 9 * * 1-5',  # Cron: 9 AM, Monday-Friday
    catchup=False,
    tags=['scheduling', 'cron', 'weekday'],
)

weekday_task = PythonOperator(
    task_id='weekday_task',
    python_callable=weekday_task_function,
    dag=weekday_dag,
)

#Custom Timedelta Schedule (Every 6 hours)
def custom_interval_task_function(**context):
    print(f"Custom interval task running at: {datetime.now()}")
    print(f"This runs every 6 hours")
    return "custom_complete"

custom_dag = DAG(
    'custom_interval_demo',
    default_args={
        'owner': 'htunhtunhtet',
        'depends_on_past': False,
        'start_date': pendulum.datetime(2024, 1, 1, tz="UTC"),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description='Custom 6-hour interval',
    schedule_interval=timedelta(hours=6),  # Every 6 hours
    catchup=False,
    tags=['scheduling', 'custom-interval'],
)

custom_task = PythonOperator(
    task_id='custom_interval_task',
    python_callable=custom_interval_task_function,
    dag=custom_dag,
)