from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.api.api_ingestor import APIIngestor
from ingestion.csv.csv_ingestor import CSVIngestor
from ingestion.postgres.postgres_ingestor import PostgreSQLIngestor


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def ingest_api_data():
    """Ingest data from Mock API"""
    print("Starting API ingestion...")
    
    api_ingestor = APIIngestor(
        base_url="http://mock-api:5000/api/v1",
        output_dir="data/raw/api"
    )
    
    # Ingest customers
    api_ingestor.ingest_customers()
    
    # Ingest products
    api_ingestor.ingest_products()
    
    # Ingest stores
    api_ingestor.ingest_stores()
    
    print("API ingestion complete!")


def ingest_csv_data():
    """Ingest data from CSV files"""
    print("Starting CSV ingestion...")
    
    csv_ingestor = CSVIngestor(
        input_dir="data/incoming",
        output_dir="data/raw/csv"
    )
    
    # Ingest orders
    csv_ingestor.ingest_orders()
    
    # Ingest line items
    csv_ingestor.ingest_line_items()
    
    # Ingest returns
    csv_ingestor.ingest_returns()
    
    print("CSV ingestion complete!")


def ingest_postgres_data():
    """Ingest data from PostgreSQL"""
    print("Starting PostgreSQL ingestion...")
    
    postgres_ingestor = PostgreSQLIngestor(
        host="retailpulse-postgres-ops",
        port=5432,
        database="retail_ops",
        user="retail_user",
        password=os.getenv("POSTGRES_PASSWORD", "retail_secure_password_2024"),
        output_dir="data/raw/postgres"
    )
    
    # Ingest customers
    postgres_ingestor.ingest_customers()
    
    # Ingest products
    postgres_ingestor.ingest_products()
    
    # Ingest stores
    postgres_ingestor.ingest_stores()
    
    # Ingest transactions
    postgres_ingestor.ingest_transactions()
    
    print("PostgreSQL ingestion complete!")


dag_ingestion = DAG(
    'retail_ingestion_dag',
    default_args=default_args,
    description='Ingest data from API, CSV, and PostgreSQL sources',
    schedule_interval='@daily',
    catchup=False,
    tags=['retail', 'ingestion', 'raw'],
)

# Define tasks
ingest_api_task = PythonOperator(
    task_id='ingest_api_data',
    python_callable=ingest_api_data,
    dag=dag_ingestion,
)

ingest_csv_task = PythonOperator(
    task_id='ingest_csv_data',
    python_callable=ingest_csv_data,
    dag=dag_ingestion,
)

ingest_postgres_task = PythonOperator(
    task_id='ingest_postgres_data',
    python_callable=ingest_postgres_data,
    dag=dag_ingestion,
)

# Set task dependencies (run in parallel)
[ingest_api_task, ingest_csv_task, ingest_postgres_task]