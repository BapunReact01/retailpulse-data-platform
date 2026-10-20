from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retailpyspark.jobs.silver.silver_customers import SilverCustomersJob
from retailpyspark.jobs.silver.silver_products import SilverProductsJob
from retailpyspark.jobs.silver.silver_sales import SilverSalesJob


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def process_silver_customers():
    """Process customer data to Silver layer"""
    print("Starting Silver customer processing...")
    
    silver_job = SilverCustomersJob(
        input_path="data/bronze/api",
        output_path="data/silver/customers"
    )
    silver_job.run()
    
    print("Silver customer processing complete!")


def process_silver_products():
    """Process product data to Silver layer"""
    print("Starting Silver product processing...")
    
    silver_job = SilverProductsJob(
        input_path="data/bronze/api",
        output_path="data/silver/products"
    )
    silver_job.run()
    
    print("Silver product processing complete!")


def process_silver_sales():
    """Process sales data to Silver layer"""
    print("Starting Silver sales processing...")
    
    silver_job = SilverSalesJob(
        input_path="data/bronze/csv",
        output_path="data/silver/sales"
    )
    silver_job.run()
    
    print("Silver sales processing complete!")


dag_silver = DAG(
    'retail_silver_dag',
    default_args=default_args,
    description='Process Bronze data to Silver layer with transformations and enrichment',
    schedule_interval='@daily',
    catchup=False,
    tags=['retail', 'silver', 'transformation'],
)

# Define tasks
silver_customers_task = PythonOperator(
    task_id='process_silver_customers',
    python_callable=process_silver_customers,
    dag=dag_silver,
)

silver_products_task = PythonOperator(
    task_id='process_silver_products',
    python_callable=process_silver_products,
    dag=dag_silver,
)

silver_sales_task = PythonOperator(
    task_id='process_silver_sales',
    python_callable=process_silver_sales,
    dag=dag_silver,
)

# Set task dependencies (run in parallel)
[silver_customers_task, silver_products_task, silver_sales_task]