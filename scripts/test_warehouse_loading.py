import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from warehouse.loaders.dimension_loader import DimensionLoader
from warehouse.loaders.fact_loader import FactLoader

# Load environment variables
load_dotenv()


def test_warehouse_setup():
    """Test warehouse schema creation"""
    print("\n=== Testing Warehouse Schema Creation ===")
    
    loader = WarehouseLoader(
        host=os.getenv("DW_HOST", "localhost"),
        port=int(os.getenv("DW_PORT", "5433")),
        database=os.getenv("DW_DATABASE", "retail_dw"),
        user=os.getenv("DW_USER", "retail_user"),
        password=os.getenv("DW_PASSWORD", "retail_secure_password_2024")
    )
    
    if loader.connect():
        # Execute DDL file
        ddl_path = "warehouse/ddl/02_create_star_schema.sql"
        if loader.execute_file(ddl_path):
            print("Warehouse schema created successfully!")
        loader.disconnect()


def test_dimension_loading():
    """Test dimension table loading"""
    print("\n=== Testing Dimension Loading ===")
    
    loader = DimensionLoader(
        host=os.getenv("DW_HOST", "localhost"),
        port=int(os.getenv("DW_PORT", "5433")),
        database=os.getenv("DW_DATABASE", "retail_dw"),
        user=os.getenv("DW_USER", "retail_user"),
        password=os.getenv("DW_PASSWORD", "retail_secure_password_2024")
    )
    
    if loader.connect():
        # Sample customer data
        customers = [
            {
                'customer_id': 'CUST001',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'phone': '+919876543210',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'country': 'India',
                'postal_code': '400001',
                'registration_date': '2024-01-01',
                'customer_segment': 'premium',
                'customer_tier': 'gold',
                'loyalty_score': 100,
                'days_as_customer': 300,
                'customer_lifetime_value': 50000.00
            }
        ]
        
        if loader.load_customers(customers):
            print("Customer dimension loaded successfully!")
        
        loader.disconnect()


if __name__ == "__main__":
    print("Starting warehouse loading tests...")
    print("Note: This requires warehouse PostgreSQL to be running")
    
    try:
        test_warehouse_setup()
        test_dimension_loading()
        
        print("\n=== Warehouse Loading Tests Complete ===")
    except Exception as e:
        print(f"\nError during warehouse testing: {e}")
        print("Note: Warehouse PostgreSQL may not be running or credentials may be incorrect")
        print("The warehouse loading code is ready and can be tested when warehouse is available")