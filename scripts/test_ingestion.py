import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ingestion.api.api_ingestor import APIIngestor
from ingestion.csv.csv_ingestor import CSVIngestor
from ingestion.postgres.postgres_ingestor import PostgresIngestor


def test_api_ingestion():
    """Test API ingestion from Mock API"""
    print("\n=== Testing API Ingestion ===")
    
    # Test customers
    customers_ingestor = APIIngestor(
        base_url="http://localhost:5000/api/v1/customers",
        source_name="customers_api",
        output_path="data/raw/api"
    )
    customers_file = customers_ingestor.ingest(format='json')
    print(f"Customers API: {customers_file}")
    
    # Test products
    products_ingestor = APIIngestor(
        base_url="http://localhost:5000/api/v1/products",
        source_name="products_api",
        output_path="data/raw/api"
    )
    products_file = products_ingestor.ingest(format='json')
    print(f"Products API: {products_file}")
    
    # Test stores
    stores_ingestor = APIIngestor(
        base_url="http://localhost:5000/api/v1/stores",
        source_name="stores_api",
        output_path="data/raw/api"
    )
    stores_file = stores_ingestor.ingest(format='json')
    print(f"Stores API: {stores_file}")


def test_csv_ingestion():
    """Test CSV ingestion"""
    print("\n=== Testing CSV Ingestion ===")
    
    # Test orders
    orders_ingestor = CSVIngestor(
        source_path="data/incoming/orders/orders_2026-10-11.csv",
        source_name="orders_csv",
        output_path="data/raw/csv"
    )
    orders_file = orders_ingestor.ingest(format='json')
    print(f"Orders CSV: {orders_file}")
    
    # Test line items
    line_items_ingestor = CSVIngestor(
        source_path="data/incoming/line_items/line_items_2026-10-11.csv",
        source_name="line_items_csv",
        output_path="data/raw/csv"
    )
    line_items_file = line_items_ingestor.ingest(format='json')
    print(f"Line Items CSV: {line_items_file}")
    
    # Test returns
    returns_ingestor = CSVIngestor(
        source_path="data/incoming/returns/returns_2026-10-11.csv",
        source_name="returns_csv",
        output_path="data/raw/csv"
    )
    returns_file = returns_ingestor.ingest(format='json')
    print(f"Returns CSV: {returns_file}")


def test_postgres_ingestion():
    """Test PostgreSQL ingestion"""
    print("\n=== Testing PostgreSQL Ingestion ===")
    
    postgres_ingestor = PostgresIngestor(
        host="localhost",
        port=5432,
        database="retail_ops",
        user="retail_user",
        password="retail_secure_password_2024",
        source_name="postgres_ops",
        output_path="data/raw/postgres"
    )
    
    # Test customers table
    customers_data = postgres_ingestor.extract_table("customers")
    if customers_data:
        postgres_ingestor.save_to_json(customers_data, "customers.json")
    
    # Test products table
    products_data = postgres_ingestor.extract_table("products")
    if products_data:
        postgres_ingestor.save_to_json(products_data, "products.json")
    
    # Test stores table
    stores_data = postgres_ingestor.extract_table("stores")
    if stores_data:
        postgres_ingestor.save_to_json(stores_data, "stores.json")
    
    # Test transactions table
    transactions_data = postgres_ingestor.extract_table("transactions")
    if transactions_data:
        postgres_ingestor.save_to_json(transactions_data, "transactions.json")


if __name__ == "__main__":
    print("Starting ingestion tests...")
    
    test_api_ingestion()
    test_csv_ingestion()
    test_postgres_ingestion()
    
    print("\n=== All Ingestion Tests Complete ===")