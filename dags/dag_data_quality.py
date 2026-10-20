from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_quality.validators import DataValidator
from data_quality.quarantine import QuarantineHandler
from data_quality.quality_report import QualityReport


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def check_bronze_quality():
    """Check Bronze layer data quality"""
    print("Starting Bronze quality check...")
    
    validator = DataValidator()
    quarantine = QuarantineHandler()
    report = QualityReport()
    
    # In production, this would read Bronze Parquet files
    print("Checking Bronze layer quality...")
    
    stats = validator.get_statistics()
    report.generate_report('bronze', stats, validator.violations)
    
    print(f"Bronze quality check: {stats['validity_rate']:.2f}% valid")


def check_silver_quality():
    """Check Silver layer data quality"""
    print("Starting Silver quality check...")
    
    validator = DataValidator()
    quarantine = QuarantineHandler()
    report = QualityReport()
    
    # In production, this would read Silver Parquet files
    print("Checking Silver layer quality...")
    
    stats = validator.get_statistics()
    report.generate_report('silver', stats, validator.violations)
    
    print(f"Silver quality check: {stats['validity_rate']:.2f}% valid")


def check_gold_quality():
    """Check Gold layer data quality"""
    print("Starting Gold quality check...")
    
    validator = DataValidator()
    quarantine = QuarantineHandler()
    report = QualityReport()
    
    # In production, this would read Gold Parquet files
    print("Checking Gold layer quality...")
    
    stats = validator.get_statistics()
    report.generate_report('gold', stats, validator.violations)
    
    print(f"Gold quality check: {stats['validity_rate']:.2f}% valid")


def check_warehouse_quality():
    """Check Warehouse data quality"""
    print("Starting Warehouse quality check...")
    
    # In production, this would check referential integrity
    print("Checking Warehouse referential integrity...")
    
    print("Warehouse quality check complete!")


dag_data_quality = DAG(
    'retail_data_quality_dag',
    default_args=default_args,
    description='Run data quality checks on all layers',
    schedule_interval='@daily',
    catchup=False,
    tags=['retail', 'quality', 'validation'],
)

# Define tasks
bronze_quality_task = PythonOperator(
    task_id='check_bronze_quality',
    python_callable=check_bronze_quality,
    dag=dag_data_quality,
)

silver_quality_task = PythonOperator(
    task_id='check_silver_quality',
    python_callable=check_silver_quality,
    dag=dag_data_quality,
)

gold_quality_task = PythonOperator(
    task_id='check_gold_quality',
    python_callable=check_gold_quality,
    dag=dag_data_quality,
)

warehouse_quality_task = PythonOperator(
    task_id='check_warehouse_quality',
    python_callable=check_warehouse_quality,
    dag=dag_data_quality,
)

# Set task dependencies (run in parallel)
[bronze_quality_task, silver_quality_task, gold_quality_task, warehouse_quality_task]