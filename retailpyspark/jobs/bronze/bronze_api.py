from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from retailpyspark.utils.spark_utils import SparkUtils
import json
import os


class BronzeAPIJob:
    """Bronze layer job for API data ingestion"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("BronzeAPIJob")
    
    def process_customers(self):
        """Process customers data from API"""
        print("Processing customers data...")
        
        # Read JSON file
        customers_file = os.path.join(self.input_path, "customers_api_*.json")
        customers_data = []
        
        for file in os.listdir(self.input_path):
            if "customers_api" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if 'data' in data:
                        customers_data.extend(data['data'])
        
        if not customers_data:
            print("No customers data found")
            return None
        
        # Create DataFrame
        df = self.spark.createDataFrame(customers_data)
        
        # Add audit columns
        df = SparkUtils.add_audit_columns(df, "api")
        
        # Deduplicate on customer_id
        df = SparkUtils.deduplicate(df, ["customer_id"])
        
        # Handle nulls
        df = SparkUtils.handle_nulls(df, ["email", "phone"])
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "customers")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} customers to {output_file}")
        return output_file
    
    def process_products(self):
        """Process products data from API"""
        print("Processing products data...")
        
        products_data = []
        for file in os.listdir(self.input_path):
            if "products_api" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if 'data' in data:
                        products_data.extend(data['data'])
        
        if not products_data:
            print("No products data found")
            return None
        
        df = self.spark.createDataFrame(products_data)
        df = SparkUtils.add_audit_columns(df, "api")
        df = SparkUtils.deduplicate(df, ["product_id"])
        df = SparkUtils.handle_nulls(df, ["brand"])
        
        output_file = os.path.join(self.output_path, "products")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} products to {output_file}")
        return output_file
    
    def process_stores(self):
        """Process stores data from API"""
        print("Processing stores data...")
        
        stores_data = []
        for file in os.listdir(self.input_path):
            if "stores_api" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if 'data' in data:
                        stores_data.extend(data['data'])
        
        if not stores_data:
            print("No stores data found")
            return None
        
        df = self.spark.createDataFrame(stores_data)
        df = SparkUtils.add_audit_columns(df, "api")
        df = SparkUtils.deduplicate(df, ["store_id"])
        df = SparkUtils.handle_nulls(df, ["manager_name"])
        
        output_file = os.path.join(self.output_path, "stores")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} stores to {output_file}")
        return output_file
    
    def run(self):
        """Run all Bronze API processing"""
        print("Starting Bronze API processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_customers()
        self.process_products()
        self.process_stores()
        
        self.spark.stop()
        print("Bronze API processing complete!")
