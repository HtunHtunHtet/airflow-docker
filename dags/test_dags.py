import unittest
from datetime import datetime, timedelta
from airflow.models import DagBag
from airflow.utils.dates import days_ago
from airflow.utils.state import State
from airflow import DAG
from airflow.operators.python import PythonOperator

# Import your DAGs to test
import sys
import os
sys.path.append('/opt/airflow/dags')

class TestProductDescriptionPOC(unittest.TestCase):
    """
    Test cases for the product_description_poc DAG
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.dagbag = DagBag()
        self.dag_id = 'product_description_poc'
        self.dag = self.dagbag.get_dag(self.dag_id)

    def test_dag_loaded(self):
        """Test that the DAG is loaded correctly"""
        self.assertIsNotNone(self.dag)
        self.assertEqual(self.dag.dag_id, self.dag_id)

    def test_dag_has_correct_number_of_tasks(self):
        """Test that DAG has expected number of tasks"""
        self.assertEqual(len(self.dag.tasks), 3)

    def test_dag_has_correct_tasks(self):
        """Test that DAG contains expected tasks"""
        task_ids = [task.task_id for task in self.dag.tasks]
        expected_tasks = ['fetch_product_data', 'generate_description', 'save_description']

        for task in expected_tasks:
            self.assertIn(task, task_ids)

    def test_task_dependencies(self):
        """Test that task dependencies are correct"""
        fetch_task = self.dag.get_task('fetch_product_data')
        generate_task = self.dag.get_task('generate_description')
        save_task = self.dag.get_task('save_description')

        # Check upstream dependencies
        self.assertEqual(len(fetch_task.upstream_task_ids), 0)
        self.assertEqual(len(generate_task.upstream_task_ids), 1)
        self.assertEqual(len(save_task.upstream_task_ids), 1)

        # Check downstream dependencies
        self.assertIn('generate_description', fetch_task.downstream_task_ids)
        self.assertIn('save_description', generate_task.downstream_task_ids)

    def test_dag_schedule_interval(self):
        """Test that DAG has correct schedule"""
        self.assertIsNone(self.dag.schedule_interval)  # Manual trigger only

    def test_dag_catchup_setting(self):
        """Test that catchup is disabled"""
        self.assertFalse(self.dag.catchup)

class TestTaskFunctions(unittest.TestCase):
    """
    Test individual task functions
    """

    def test_fetch_product_data_function(self):
        """Test the fetch_product_data function directly"""
        # Import the function
        from product_description_poc import fetch_product_data

        # Test the function
        result = fetch_product_data()

        # Assertions
        self.assertIsInstance(result, dict)
        self.assertIn('product_id', result)
        self.assertIn('name', result)
        self.assertEqual(result['product_id'], '123')
        self.assertEqual(result['name'], 'Test Product')

class TestDynamicDAGs(unittest.TestCase):
    """
    Test dynamically generated DAGs
    """

    def setUp(self):
        self.dagbag = DagBag()
        self.expected_categories = ['electronics', 'clothing', 'books']

    def test_dynamic_dags_created(self):
        """Test that all dynamic DAGs were created"""
        for category in self.expected_categories:
            dag_id = f'product_pipeline_{category}'
            dag = self.dagbag.get_dag(dag_id)
            self.assertIsNotNone(dag, f"DAG {dag_id} should exist")

    def test_dynamic_dag_schedules(self):
        """Test that dynamic DAGs have correct schedules"""
        expected_schedules = {
            'electronics': '@daily',
            'clothing': '@hourly',
            'books': None
        }

        for category, expected_schedule in expected_schedules.items():
            dag_id = f'product_pipeline_{category}'
            dag = self.dagbag.get_dag(dag_id)
            self.assertEqual(dag.schedule_interval, expected_schedule)

    def test_dynamic_dag_tags(self):
        """Test that dynamic DAGs have correct tags"""
        for category in self.expected_categories:
            dag_id = f'product_pipeline_{category}'
            dag = self.dagbag.get_dag(dag_id)

            expected_tags = ['dynamic', 'product-pipeline', category]
            for tag in expected_tags:
                self.assertIn(tag, dag.tags)

class TestDAGBagIntegrity(unittest.TestCase):
    """
    Test overall DAG bag integrity
    """

    def setUp(self):
        self.dagbag = DagBag()

    def test_no_import_errors(self):
        """Test that there are no DAG import errors"""
        self.assertEqual(len(self.dagbag.import_errors), 0,
                        f"DAG import errors: {self.dagbag.import_errors}")

    def test_all_dags_have_owners(self):
        """Test that all DAGs have owners set"""
        for dag_id, dag in self.dagbag.dags.items():
            if dag_id.startswith(('product_', 'custom_', 'sensors_', 'dynamic_')):
                self.assertIsNotNone(dag.default_args.get('owner'))
                self.assertNotEqual(dag.default_args.get('owner'), '')

# Test runner function
def run_tests():
    """
    Function to run all tests - can be called from a PythonOperator
    """
    import io
    import sys

    # Capture test output
    test_output = io.StringIO()
    runner = unittest.TextTestRunner(stream=test_output, verbosity=2)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestProductDescriptionPOC))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskFunctions))
    suite.addTests(loader.loadTestsFromTestCase(TestDynamicDAGs))
    suite.addTests(loader.loadTestsFromTestCase(TestDAGBagIntegrity))

    # Run tests
    result = runner.run(suite)

    # Print results
    output = test_output.getvalue()
    print(output)

    # Return summary
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'success': result.wasSuccessful()
    }

if __name__ == '__main__':
    # Run tests when executed directly
    run_tests()


    # Create a DAG that runs the tests
test_dag = DAG(
    'run_dag_tests',
    default_args={
        'owner': 'htunhtunhtet',
        'start_date': datetime(2024, 1, 1),
    },
    description='Run DAG tests',
    schedule_interval=None,
    catchup=False,
    tags=['testing'],
)

# Task to run tests
run_tests_task = PythonOperator(
    task_id='run_all_tests',
    python_callable=run_tests,
    dag=test_dag,
)

