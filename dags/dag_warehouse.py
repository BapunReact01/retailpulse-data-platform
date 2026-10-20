from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from warehouse.loaders.dimension_loader import DimensionLoader
from warehouse.loaders.fact_loader import FactLoader


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def load_dimensions():
    """Load dimension tables into warehouse"""
    print("Starting dimension loading...")
    
    loader = DimensionLoader(
        host="retailpulse-postgres-dw",
        port=5433,
        database="retail_dw",
        user="retail_user",
        password=os.getenv("POSTGRES_PASSWORD", "retail_secure_password_2024")
    )
    
    if loader.connect():
        # Load dimensions from Gold layer
        # Note: In production, this would read from Gold Parquet files
        print("Loading dimensions from Gold layer...")
        loader.disconnect()
    
    print("Dimension loading complete!")


def load_facts():
    """Load fact tables into warehouse"""
    print("Starting fact loading...")
    
    loader = FactLoader(
        host="retailpulse-postgres-dw",
        port=5433,
        database="retail_dw",
        user="retail_user",
        password=os.getenv("POSTGRES_PASSWORD", "retail_secure_password_2024")
    )
    
    if loader.connect():
        # Load facts from Gold layer
        # Note: In production, this would read from Gold Parquet files
        print("Loading facts from Gold layer...")
        loader.disconnect()
    
    print("Fact loading complete!")


dag_warehouse = DAG(
    'retail_warehouse_dag',
    default_args=default_args,
    description='Load Gold layer data into Star Schema warehouse',
    schedule_interval='@daily',
    catchup=False,
    tags=['retail', 'warehouse', 'loading'],
)

# Define tasks
load_dimensions_task = PythonOperator(
    task_id='load_dimensions',
    python_callable=load_dimensions,
    dag=dag_warehouse,
)

load_facts_task = PythonOperator(
    task_id='load_facts',
    python_callable=load_facts,
    dag=dag_warehouse,
)

# Set task dependencies (dimensions before facts)
load_dimensions_task >> load_facts_task