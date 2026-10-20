from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from retailpyspark.jobs.bronze.bronze_api import BronzeAPIJob
from retailpyspark.jobs.bronze.bronze_csv import BronzeCSVJob
from retailpyspark.jobs.bronze.bronze_postgres import BronzePostgresJob


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def process_bronze_api():
    """Process API data to Bronze layer"""
    print("Starting Bronze API processing...")
    
    bronze_job = BronzeAPIJob(
        input_path="data/raw/api",
        output_path="data/bronze/api"
    )
    bronze_job.run()
    
    print("Bronze API processing complete!")


def process_bronze_csv():
    """Process CSV data to Bronze layer"""
    print("Starting Bronze CSV processing...")
    
    bronze_job = BronzeCSVJob(
        input_path="data/raw/csv",
        output_path="data/bronze/csv"
    )
    bronze_job.run()
    
    print("Bronze CSV processing complete!")


def process_bronze_postgres():
    """Process PostgreSQL data to Bronze layer"""
    print("Starting Bronze PostgreSQL processing...")
    
    bronze_job = BronzePostgresJob(
        input_path="data/raw/postgres",
        output_path="data/bronze/postgres"
    )
    bronze_job.run()
    
    print("Bronze PostgreSQL processing complete!")


dag_bronze = DAG(
    'retail_bronze_dag',
    default_args=default_args,
    description='Process raw data to Bronze layer with cleansing and validation',
    schedule_interval='@daily',
    catchup=False,
    tags=['retail', 'bronze', 'cleansing'],
)

# Define tasks
bronze_api_task = PythonOperator(
    task_id='process_bronze_api',
    python_callable=process_bronze_api,
    dag=dag_bronze,
)

bronze_csv_task = PythonOperator(
    task_id='process_bronze_csv',
    python_callable=process_bronze_csv,
    dag=dag_bronze,
)

bronze_postgres_task = PythonOperator(
    task_id='process_bronze_postgres',
    python_callable=process_bronze_postgres,
    dag=dag_bronze,
)

# Set task dependencies (run in parallel)
[bronze_api_task, bronze_csv_task, bronze_postgres_task]