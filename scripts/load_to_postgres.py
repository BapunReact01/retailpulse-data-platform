import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'retail_dw',
    'user': 'retail_user',
    'password': os.getenv('POSTGRES_PASSWORD', 'retail_secure_password_2024')
}

def create_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)

def create_tables(conn):
    """Create tables in warehouse"""
    cursor = conn.cursor()
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id VARCHAR(20) PRIMARY KEY,
            signup_date DATE,
            region VARCHAR(50),
            segment VARCHAR(20),
            lifetime_orders INTEGER,
            lifetime_spend DECIMAL(15, 2),
            email_domain VARCHAR(100)
        )
    """)
    
    # Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id VARCHAR(20) PRIMARY KEY,
            category VARCHAR(50),
            subcategory VARCHAR(50),
            price DECIMAL(10, 2),
            cost DECIMAL(10, 2),
            brand VARCHAR(100),
            launch_date DATE,
            avg_rating DECIMAL(3, 2)
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id VARCHAR(20) PRIMARY KEY,
            customer_id VARCHAR(20),
            session_id VARCHAR(50),
            order_date DATE,
            status VARCHAR(20),
            item_count INTEGER,
            order_total DECIMAL(15, 2),
            payment_method VARCHAR(50)
        )
    """)
    
    # Create order_items table (FIXED: VARCHAR(50) instead of VARCHAR(20))
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id VARCHAR(50) PRIMARY KEY,
            order_id VARCHAR(20),
            product_id VARCHAR(20),
            quantity INTEGER,
            unit_price DECIMAL(10, 2),
            line_total DECIMAL(15, 2)
        )
    """)
    
    conn.commit()
    print("✅ Tables created successfully")

def load_customers(conn, input_path, batch_size=50000):
    """Load customers data in batches"""
    print("Loading customers...")
    df = pd.read_parquet(f"{input_path}/customers.parquet")
    
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO customers (customer_id, signup_date, region, segment, lifetime_orders, lifetime_spend, email_domain)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (customer_id) DO NOTHING
    """
    
    # Load in batches
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        data = batch[['customer_id', 'signup_date', 'region', 'segment', 'lifetime_orders', 'lifetime_spend', 'email_domain']].values.tolist()
        execute_batch(cursor, insert_query, data)
        conn.commit()
        print(f"  Progress: {min(i+batch_size, len(df))}/{len(df)} customers")
    
    print(f"✅ Loaded {len(df)} customers")

def load_products(conn, input_path, batch_size=50000):
    """Load products data in batches"""
    print("Loading products...")
    df = pd.read_parquet(f"{input_path}/products.parquet")
    
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO products (product_id, category, subcategory, price, cost, brand, launch_date, avg_rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO NOTHING
    """
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        data = batch[['product_id', 'category', 'subcategory', 'price', 'cost', 'brand', 'launch_date', 'avg_rating']].values.tolist()
        execute_batch(cursor, insert_query, data)
        conn.commit()
        print(f"  Progress: {min(i+batch_size, len(df))}/{len(df)} products")
    
    print(f"✅ Loaded {len(df)} products")

def load_orders(conn, input_path, batch_size=50000):
    """Load orders data in batches"""
    print("Loading orders...")
    df = pd.read_parquet(f"{input_path}/orders.parquet")
    
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO orders (order_id, customer_id, session_id, order_date, status, item_count, order_total, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
    """
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        data = batch[['order_id', 'customer_id', 'session_id', 'order_date', 'status', 'item_count', 'order_total', 'payment_method']].values.tolist()
        execute_batch(cursor, insert_query, data)
        conn.commit()
        print(f"  Progress: {min(i+batch_size, len(df))}/{len(df)} orders")
    
    print(f"✅ Loaded {len(df)} orders")

def load_order_items(conn, input_path, batch_size=50000):
    """Load order items data in batches"""
    print("Loading order items...")
    df = pd.read_parquet(f"{input_path}/order_items.parquet")
    
    cursor = conn.cursor()
    
    insert_query = """
        INSERT INTO order_items (order_item_id, order_id, product_id, quantity, unit_price, line_total)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        data = batch[['order_item_id', 'order_id', 'product_id', 'quantity', 'unit_price', 'line_total']].values.tolist()
        execute_batch(cursor, insert_query, data)
        conn.commit()
        print(f"  Progress: {min(i+batch_size, len(df))}/{len(df)} order items")
    
    print(f"✅ Loaded {len(df)} order items")

def main():
    """Main function"""
    input_path = "data/large_dataset"
    
    print("=" * 60)
    print("Loading FreeEcommerceTwin14M Dataset to PostgreSQL")
    print("Estimated time: 20-40 minutes")
    print("=" * 60)
    
    try:
        conn = create_connection()
        create_tables(conn)
        
        load_customers(conn, input_path, batch_size=50000)
        load_products(conn, input_path, batch_size=50000)
        load_orders(conn, input_path, batch_size=50000)
        load_order_items(conn, input_path, batch_size=50000)
        
        conn.close()
        
        print("=" * 60)
        print("✅ All data loaded successfully to PostgreSQL!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()