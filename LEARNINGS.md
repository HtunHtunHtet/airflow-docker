# My Airflow Learning Experience

## What I Accomplished

Over the past 3 days, I dove into Apache Airflow to understand if it's the right tool for our product description pipeline. Here's what I learned and built during this spike.

## Getting Started - The Setup Journey

Setting up Airflow locally was more involved than I expected. I used Docker Compose which worked well, but ran into some issues:

- The `airflow-init` container kept failing initially - had to bypass it to get things running
- Started with `CeleryExecutor` but it was eating up CPU with the worker containers
- Switched to `LocalExecutor` which works much better for development
- Had to figure out the right startup sequence: database services first, then Airflow components

The final setup I landed on runs just the essential services (webserver, scheduler, MySQL, Redis) which is much more resource-friendly.

## Understanding DAGs - The Core Concept

DAGs are basically workflow definitions. I created several to test different concepts:

**product_description_poc** - This is the main one that simulates our pipeline:
- Fetches product data 
- Generates description 
- Saves the result 

**traditional_operators** - Helped me understand the difference between TaskFlow API and traditional operators

**error_handling_demo** - Tested retry mechanisms and failure scenarios

**scheduling_demo** - Played with different scheduling options

The key insight: DAGs define the structure and dependencies, but don't contain the actual business logic.

## Two Ways to Write Tasks

I learned there are basically two approaches:

### TaskFlow API (Modern)
```python
@task()
def my_function():
    return "some data"
```
This is cleaner and handles XCom automatically. Data flows naturally between functions.

### Traditional Operators
```python
PythonOperator(
    task_id='my_task',
    python_callable=my_function,
    dag=dag
)
```
More verbose but gives you more control. You have to manually handle XCom with `xcom_push()` and `xcom_pull()`.

I prefer TaskFlow for new development, but traditional operators are still widely used.

## Data Passing Between Tasks

This was trickier than expected. XCom (cross-communication) is how tasks share data:

- **TaskFlow API**: Just return values from functions and use them as parameters
- **Traditional**: Manually push/pull data using task instance context

Important limitation I discovered: XCom is only for small data (under 48KB typically). For larger datasets, you need to use external storage and pass references.

## Scheduling - More Flexible Than Expected

I experimented with different scheduling options:

- `schedule_interval=None` - Manual triggers only (great for testing)
- `@daily`, `@hourly` - Preset schedules
- `timedelta(hours=6)` - Custom intervals  
- `'0 9 * * 1-5'` - Cron expressions (9 AM weekdays)

Pro tip: Always set `catchup=False` unless you actually want to backfill historical runs. I learned this the hard way when my DAG started running hundreds of times!

## Error Handling and Retries

The retry mechanism is pretty robust:
- Set `retries` and `retry_delay` in default_args
- Individual tasks can override these settings
- Use `trigger_rule='all_done'` for cleanup tasks that should run regardless of failures

I built an error handling demo that randomly fails 70% of the time to test this - works well.

## The Airflow UI

The web interface is actually quite good:
- Easy to see DAG structure and dependencies
- Can manually trigger DAGs and individual tasks
- Task logs are accessible and helpful for debugging
- XCom tab shows data passed between tasks
- Can clear task states and rerun things

Login is airflow/airflow by default (obviously need to change for production).

## What I Built - The POC

The main deliverable is `product_description_poc.py` which demonstrates:

1. **fetch_product_data()** - Simulates getting product info from database
2. **generate_description()** - Simulates AI/ML description generation  
3. **save_description()** - Simulates storing the result

Uses traditional XCom approach since that's what the team example showed. Data flows: product data → description → save confirmation.

## Development Workflow I Established

1. Write DAG file in `/dags` folder
2. Airflow automatically picks it up (takes 30-60 seconds)
3. Enable the DAG in UI
4. Test with manual triggers
5. Check logs, diagrams and XCom data
6. Iterate and improve

## Things That Surprised Me

**Good surprises:**
- Airflow UI is more user-friendly than expected
- TaskFlow API makes simple pipelines very clean
- Retry and error handling works well out of the box
- Docker setup, once working, is quite stable

**Challenges:**
- Initial setup was fiddly (init container issues)
- Need to research regarding about which docker-compose have to use 
- XCom size limitations could be a problem for us
- Resource usage with full setup (workers, triggerer) was high
- Some concepts (executors, connections) have a learning curve

## Files Created

- `product_description_poc.py` - Main POC demonstrating our pipeline
- `traditional_operators.py` - Learning traditional operator patterns
- `error_handling_demo.py` - Testing retry and failure scenarios  
- `scheduling_demo.py` - Various scheduling examples
- `xcom_demo.py` - Data passing examples
- Plus several others for learning different concepts

All DAGs are working and can be triggered manually. The POC successfully demonstrates the fetch → generate → save pattern we need.