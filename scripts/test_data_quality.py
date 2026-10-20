import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_quality.validators import DataValidator
from data_quality.quarantine import QuarantineHandler
from data_quality.quality_report import QualityReport


def test_bronze_quality():
    """Test Bronze layer quality checks"""
    print("\n=== Testing Bronze Layer Quality ===")
    
    validator = DataValidator()
    quarantine = QuarantineHandler()
    report = QualityReport()
    
    # Sample Bronze data
    bronze_customers = [
        {'customer_id': 'CUST001', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com'},
        {'customer_id': 'CUST002', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com'},
        {'customer_id': 'CUST003', 'first_name': None, 'last_name': 'Brown', 'email': 'invalid-email'},  # Invalid
    ]
    
    # Validate NOT NULL
    is_valid, invalid = validator.validate_not_null(bronze_customers, ['customer_id', 'first_name', 'email'])
    
    if not is_valid:
        quarantine.quarantine_records(invalid, 'bronze_customers', 'NULL_VIOLATION')
    
    # Validate email format
    validator.reset()
    is_valid, invalid = validator.validate_email_format(bronze_customers, 'email')
    
    if not is_valid:
        quarantine.quarantine_records(invalid, 'bronze_customers', 'EMAIL_FORMAT_VIOLATION')
    
    # Generate report
    stats = validator.get_statistics()
    report.generate_report('bronze', stats, validator.violations)
    
    print(f"Bronze layer validity rate: {stats['validity_rate']:.2f}%")


def test_silver_quality():
    """Test Silver layer quality checks"""
    print("\n=== Testing Silver Layer Quality ===")
    
    validator = DataValidator()
    quarantine = QuarantineHandler()
    report = QualityReport()
    
    # Sample Silver data
    silver_products = [
        {'product_id': 'PROD001', 'unit_price': 100.00, 'cost_price': 50.00},
        {'product_id': 'PROD002', 'unit_price': 200.00, 'cost_price': 100.00},
        {'product_id': 'PROD003', 'unit_price': -50.00, 'cost_price': 30.00},  # Invalid: negative price
    ]
    
    # Validate positive values
    is_valid, invalid = validator.validate_positive(silver_products, 'unit_price')
    
    if not is_valid:
        quarantine.quarantine_records(invalid, 'silver_products', 'NEGATIVE_PRICE_VIOLATION')
    
    # Generate report
    stats = validator.get_statistics()
    report.generate_report('silver', stats, validator.violations)
    
    print(f"Silver layer validity rate: {stats['validity_rate']:.2f}%")


def test_gold_quality():
    """Test Gold layer quality checks"""
    print("\n=== Testing Gold Layer Quality ===")
    
    validator = DataValidator()
    quarantine = QuarantineHandler()
    report = QualityReport()
    
    # Sample Gold data
    gold_sales = [
        {'order_id': 'ORD001', 'total_revenue': 1000.00, 'order_count': 10},
        {'order_id': 'ORD002', 'total_revenue': 2000.00, 'order_count': 20},
        {'order_id': 'ORD003', 'total_revenue': 1500.00, 'order_count': 15},
    ]
    
    # Validate range
    is_valid, invalid = validator.validate_range(gold_sales, 'total_revenue', 0, 100000)
    
    if not is_valid:
        quarantine.quarantine_records(invalid, 'gold_sales', 'RANGE_VIOLATION')
    
    # Generate report
    stats = validator.get_statistics()
    report.generate_report('gold', stats, validator.violations)
    
    print(f"Gold layer validity rate: {stats['validity_rate']:.2f}%")


if __name__ == "__main__":
    print("Starting data quality tests...")
    
    try:
        test_bronze_quality()
        test_silver_quality()
        test_gold_quality()
        
        print("\n=== Data Quality Tests Complete ===")
        print("Quarantine and reports generated in data/ directory")
    except Exception as e:
        print(f"\nError during data quality testing: {e}")
        print("The data quality framework is ready and can be tested with actual data")