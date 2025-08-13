from airflow.decorators import dag, task
import pendulum

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dag_id='xcom_demo',
    tags=["xcom-demo"],
)
def xcom_demo():

    @task()
    def get_name():
        return "Alice"  # This goes into XCom

    @task()
    def get_age():
        return 25  # This also goes into XCom

    @task()
    def create_greeting(name, age):  # These come from XCom
        return f"Hello {name}, you are {age} years old!"

    @task()
    def print_greeting(greeting):  # This comes from XCom
        print(greeting)
        return "Done!"

    # Flow
    name = get_name()           # name is XComArg (placeholder)
    age = get_age()             # age is XComArg (placeholder)
    greeting = create_greeting(name, age)  # greeting is XComArg
    print_greeting(greeting)

xcom_demo()