import psycopg2
from datetime import datetime
import sys
import os

# Add parent directory to path to import mock_api models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from mock_api.models.customer_data import CUSTOMERS
from mock_api.models.product_data import PRODUCTS
from mock_api.models.store_data import STORES

# Database connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'retail_ops',
    'user': 'retail_user',
    'password': 'retail_secure_password_2024'
}

def seed_customers(cursor):
    """Seed customers table"""
    print("Seeding customers...")
    for customer in CUSTOMERS:
        cursor.execute("""
            INSERT INTO customers (
                customer_id, first_name, last_name, email, phone, street, city, state,
                country, postal_code, registration_date, customer_segment, customer_tier
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING
        """, (
            customer['customer_id'], customer['first_name'], customer['last_name'],
            customer['email'], customer['phone'], customer['street'], customer['city'],
            customer['state'], customer['country'], customer['postal_code'],
            customer['registration_date'], customer['customer_segment'], customer['customer_tier']
        ))
    print(f"Seeded {len(CUSTOMERS)} customers")

def seed_products(cursor):
    """Seed products table"""
    print("Seeding products...")
    for product in PRODUCTS:
        cursor.execute("""
            INSERT INTO products (
                product_id, product_name, category, subcategory, brand,
                unit_price, cost_price, launch_date, is_active
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_id) DO NOTHING
        """, (
            product['product_id'], product['product_name'], product['category'],
            product['subcategory'], product['brand'], product['unit_price'],
            product['cost_price'], product['launch_date'], product['is_active']
        ))
    print(f"Seeded {len(PRODUCTS)} products")

def seed_stores(cursor):
    """Seed stores table"""
    print("Seeding stores...")
    for store in STORES:
        cursor.execute("""
            INSERT INTO stores (
                store_id, store_name, city, state, country, store_type,
                opening_date, manager_name, store_size_sqft
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (store_id) DO NOTHING
        """, (
            store['store_id'], store['store_name'], store['city'], store['state'],
            store['country'], store['store_type'], store['opening_date'],
            store['manager_name'], store['store_size_sqft']
        ))
    print(f"Seeded {len(STORES)} stores")

def seed_transactions(cursor):
    """Seed some sample transactions"""
    print("Seeding transactions...")
    import random
    from datetime import timedelta
    
    # Generate 50 sample transactions
    for i in range(1, 51):
        transaction_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 90))
        transaction_time = f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"
        
        cursor.execute("""
            INSERT INTO transactions (
                transaction_id, customer_id, store_id, transaction_date, transaction_time,
                transaction_type, payment_method, total_amount
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO NOTHING
        """, (
            f"TRANS{i:06d}",
            random.choice([c['customer_id'] for c in CUSTOMERS]),
            random.choice([s['store_id'] for s in STORES]),
            transaction_date.strftime("%Y-%m-%d"),
            transaction_time,
            random.choice(['sale', 'return', 'exchange']),
            random.choice(['credit_card', 'debit_card', 'cash', 'upi']),
            round(random.uniform(500, 50000), 2)
        ))
    print("Seeded 50 transactions")

def main():
    try:
        # Connect to database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Connected to PostgreSQL operational database")
        
        # Seed all tables
        seed_customers(cursor)
        seed_products(cursor)
        seed_stores(cursor)
        seed_transactions(cursor)
        
        # Commit changes
        conn.commit()
        print("\n✅ Seed data loaded successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()