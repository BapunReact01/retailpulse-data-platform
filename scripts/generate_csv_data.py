import csv
import random
from datetime import datetime, timedelta
import os

# Configuration
OUTPUT_DIR = "data/incoming"
NUM_ORDERS = 100
START_DATE = datetime(2024, 1, 1)

# Sample data
CUSTOMER_IDS = [f"CUST{i:03d}" for i in range(1, 6)]
STORE_IDS = [f"STORE{i:03d}" for i in range(1, 6)]
PRODUCT_IDS = [f"PROD{i:03d}" for i in range(1, 11)]
PAYMENT_METHODS = ["credit_card", "debit_card", "cash", "upi", "net_banking"]

def generate_orders():
    """Generate orders CSV"""
    orders = []
    for i in range(1, NUM_ORDERS + 1):
        order_date = START_DATE + timedelta(days=random.randint(0, 90))
        order = {
            "order_id": f"ORD{i:06d}",
            "customer_id": random.choice(CUSTOMER_IDS),
            "store_id": random.choice(STORE_IDS),
            "order_date": order_date.strftime("%Y-%m-%d"),
            "order_time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
            "payment_method": random.choice(PAYMENT_METHODS),
            "total_amount": round(random.uniform(500, 50000), 2),
            "status": random.choice(["completed", "pending", "cancelled"])
        }
        orders.append(order)
    
    # Write to CSV
    output_path = os.path.join(OUTPUT_DIR, "orders", f"orders_{datetime.now().strftime('%Y-%m-%d')}.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=orders[0].keys())
        writer.writeheader()
        writer.writerows(orders)
    
    print(f"Generated {len(orders)} orders to {output_path}")

def generate_line_items():
    """Generate line items CSV"""
    line_items = []
    for i in range(1, NUM_ORDERS + 1):
        order_id = f"ORD{i:06d}"
        num_items = random.randint(1, 5)
        for j in range(num_items):
            line_item = {
                "line_item_id": f"LI{i:06d}{j:02d}",
                "order_id": order_id,
                "product_id": random.choice(PRODUCT_IDS),
                "quantity": random.randint(1, 10),
                "unit_price": round(random.uniform(100, 10000), 2),
                "discount": round(random.uniform(0, 20), 2)
            }
            line_items.append(line_item)
    
    # Write to CSV
    output_path = os.path.join(OUTPUT_DIR, "line_items", f"line_items_{datetime.now().strftime('%Y-%m-%d')}.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=line_items[0].keys())
        writer.writeheader()
        writer.writerows(line_items)
    
    print(f"Generated {len(line_items)} line items to {output_path}")

def generate_returns():
    """Generate returns CSV"""
    returns = []
    num_returns = int(NUM_ORDERS * 0.1)  # 10% of orders are returns
    
    for i in range(1, num_returns + 1):
        return_date = START_DATE + timedelta(days=random.randint(0, 90))
        return_item = {
            "return_id": f"RET{i:06d}",
            "order_id": f"ORD{random.randint(1, NUM_ORDERS):06d}",
            "product_id": random.choice(PRODUCT_IDS),
            "return_date": return_date.strftime("%Y-%m-%d"),
            "reason": random.choice(["defective", "wrong_item", "not_as_described", "damaged"]),
            "refund_amount": round(random.uniform(100, 5000), 2),
            "status": random.choice(["approved", "pending", "rejected"])
        }
        returns.append(return_item)
    
    # Write to CSV
    output_path = os.path.join(OUTPUT_DIR, "returns", f"returns_{datetime.now().strftime('%Y-%m-%d')}.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=returns[0].keys())
        writer.writeheader()
        writer.writerows(returns)
    
    print(f"Generated {len(returns)} returns to {output_path}")

if __name__ == "__main__":
    print("Generating CSV data files...")
    generate_orders()
    generate_line_items()
    generate_returns()
    print("CSV generation complete!")