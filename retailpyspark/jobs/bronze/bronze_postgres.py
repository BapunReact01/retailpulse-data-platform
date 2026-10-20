from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
from retailpyspark.utils.spark_utils import SparkUtils
import json
import os


class BronzePostgresJob:
    """Bronze layer job for PostgreSQL data ingestion"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("BronzePostgresJob")
    
    def process_customers(self):
        """Process customers data from PostgreSQL"""
        print("Processing customers data from PostgreSQL...")
        
        customers_data = []
        for file in os.listdir(self.input_path):
            if "customers" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        customers_data.extend(data)
                    elif 'data' in data:
                        customers_data.extend(data['data'])
        
        if not customers_data:
            print("No customers data found")
            return None
        
        df = self.spark.createDataFrame(customers_data)
        df = SparkUtils.add_audit_columns(df, "postgres")
        df = SparkUtils.deduplicate(df, ["customer_id"])
        
        output_file = os.path.join(self.output_path, "customers")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} customers to {output_file}")
        return output_file
    
    def process_products(self):
        """Process products data from PostgreSQL"""
        print("Processing products data from PostgreSQL...")
        
        products_data = []
        for file in os.listdir(self.input_path):
            if "products" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        products_data.extend(data)
                    elif 'data' in data:
                        products_data.extend(data['data'])
        
        if not products_data:
            print("No products data found")
            return None
        
        df = self.spark.createDataFrame(products_data)
        df = SparkUtils.add_audit_columns(df, "postgres")
        df = SparkUtils.deduplicate(df, ["product_id"])
        
        # Cast price columns
        df = df.withColumn("unit_price", col("unit_price").cast("double"))
        df = df.withColumn("cost_price", col("cost_price").cast("double"))
        
        output_file = os.path.join(self.output_path, "products")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} products to {output_file}")
        return output_file
    
    def process_stores(self):
        """Process stores data from PostgreSQL"""
        print("Processing stores data from PostgreSQL...")
        
        stores_data = []
        for file in os.listdir(self.input_path):
            if "stores" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        stores_data.extend(data)
                    elif 'data' in data:
                        stores_data.extend(data['data'])
        
        if not stores_data:
            print("No stores data found")
            return None
        
        df = self.spark.createDataFrame(stores_data)
        df = SparkUtils.add_audit_columns(df, "postgres")
        df = SparkUtils.deduplicate(df, ["store_id"])
        
        output_file = os.path.join(self.output_path, "stores")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} stores to {output_file}")
        return output_file
    
    def process_transactions(self):
        """Process transactions data from PostgreSQL"""
        print("Processing transactions data from PostgreSQL...")
        
        transactions_data = []
        for file in os.listdir(self.input_path):
            if "transactions" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        transactions_data.extend(data)
                    elif 'data' in data:
                        transactions_data.extend(data['data'])
        
        if not transactions_data:
            print("No transactions data found")
            return None
        
        df = self.spark.createDataFrame(transactions_data)
        df = SparkUtils.add_audit_columns(df, "postgres")
        df = SparkUtils.deduplicate(df, ["transaction_id"])
        
        # Cast date and amount
        df = df.withColumn("transaction_date", to_timestamp("transaction_date"))
        df = df.withColumn("total_amount", col("total_amount").cast("double"))
        
        output_file = os.path.join(self.output_path, "transactions")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} transactions to {output_file}")
        return output_file
    
    def run(self):
        """Run all Bronze PostgreSQL processing"""
        print("Starting Bronze PostgreSQL processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_customers()
        self.process_products()
        self.process_stores()
        self.process_transactions()
        
        self.spark.stop()
        print("Bronze PostgreSQL processing complete!")
