from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retailpyspark.jobs.gold.gold_sales import GoldSalesJob
from retailpyspark.jobs.gold.gold_customers import GoldCustomersJob
from retailpyspark.jobs.gold.gold_products import GoldProductsJob
from retailpyspark.jobs.gold.gold_stores import GoldStoresJob


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def process_gold_sales():
    """Process sales data to Gold layer with aggregations"""
    print("Starting Gold sales processing...")
    
    gold_job = GoldSalesJob(
        input_path="data/silver/sales",
        output_path="data/gold/sales"
    )
    gold_job.run()
    
    print("Gold sales processing complete!")


def process_gold_customers():
    """Process customer analytics to Gold layer"""
    print("Starting Gold customer processing...")
    
    gold_job = GoldCustomersJob(
        input_path="data/silver/sales",
        output_path="data/gold/customers"
    )
    gold_job.run()
    
    print("Gold customer processing complete!")


def process_gold_products():
    """Process product analytics to Gold layer"""
    print("Starting Gold product processing...")
    
    gold_job = GoldProductsJob(
        input_path="data/silver/sales",
        output_path="data/gold/products"
    )
    gold_job.run()
    
    print("Gold product processing complete!")


def process_gold_stores():
    """Process store analytics to Gold layer"""
    print("Starting Gold store processing...")
    
    gold_job = GoldStoresJob(
        input_path="data/silver/sales",
        output_path="data/gold/stores"
    )
    gold_job.run()
    
    print("Gold store processing complete!")


dag_gold = DAG(
    'retail_gold_dag',
    default_args=default_args,
    description='Process Silver data to Gold layer with aggregations and KPIs',
    schedule_interval='@daily',
    catchup=False,
    tags=['retail', 'gold', 'aggregation'],
)

# Define tasks
gold_sales_task = PythonOperator(
    task_id='process_gold_sales',
    python_callable=process_gold_sales,
    dag=dag_gold,
)

gold_customers_task = PythonOperator(
    task_id='process_gold_customers',
    python_callable=process_gold_customers,
    dag=dag_gold,
)

gold_products_task = PythonOperator(
    task_id='process_gold_products',
    python_callable=process_gold_products,
    dag=dag_gold,
)

gold_stores_task = PythonOperator(
    task_id='process_gold_stores',
    python_callable=process_gold_stores,
    dag=dag_gold,
)

# Set task dependencies (run in parallel)
[gold_sales_task, gold_customers_task, gold_products_task, gold_stores_task]