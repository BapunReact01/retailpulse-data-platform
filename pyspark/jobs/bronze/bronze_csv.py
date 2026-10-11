from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp
from pyspark.utils.spark_utils import SparkUtils
import json
import os


class BronzeCSVJob:
    """Bronze layer job for CSV data ingestion"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("BronzeCSVJob")
    
    def process_orders(self):
        """Process orders data from CSV"""
        print("Processing orders data...")
        
        orders_data = []
        for file in os.listdir(self.input_path):
            if "orders_csv" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if 'data' in data:
                        orders_data.extend(data['data'])
        
        if not orders_data:
            print("No orders data found")
            return None
        
        df = self.spark.createDataFrame(orders_data)
        df = SparkUtils.add_audit_columns(df, "csv")
        df = SparkUtils.deduplicate(df, ["order_id"])
        
        # Cast date and time columns
        df = df.withColumn("order_date", to_timestamp("order_date"))
        
        output_file = os.path.join(self.output_path, "orders")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} orders to {output_file}")
        return output_file
    
    def process_line_items(self):
        """Process line items data from CSV"""
        print("Processing line items data...")
        
        line_items_data = []
        for file in os.listdir(self.input_path):
            if "line_items_csv" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if 'data' in data:
                        line_items_data.extend(data['data'])
        
        if not line_items_data:
            print("No line items data found")
            return None
        
        df = self.spark.createDataFrame(line_items_data)
        df = SparkUtils.add_audit_columns(df, "csv")
        df = SparkUtils.deduplicate(df, ["line_item_id"])
        
        # Cast numeric columns
        df = df.withColumn("quantity", col("quantity").cast("int"))
        df = df.withColumn("unit_price", col("unit_price").cast("double"))
        df = df.withColumn("discount", col("discount").cast("double"))
        
        output_file = os.path.join(self.output_path, "line_items")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} line items to {output_file}")
        return output_file
    
    def process_returns(self):
        """Process returns data from CSV"""
        print("Processing returns data...")
        
        returns_data = []
        for file in os.listdir(self.input_path):
            if "returns_csv" in file and file.endswith('.json'):
                with open(os.path.join(self.input_path, file), 'r') as f:
                    data = json.load(f)
                    if 'data' in data:
                        returns_data.extend(data['data'])
        
        if not returns_data:
            print("No returns data found")
            return None
        
        df = self.spark.createDataFrame(returns_data)
        df = SparkUtils.add_audit_columns(df, "csv")
        df = SparkUtils.deduplicate(df, ["return_id"])
        
        # Cast date and refund amount
        df = df.withColumn("return_date", to_timestamp("return_date"))
        df = df.withColumn("refund_amount", col("refund_amount").cast("double"))
        
        output_file = os.path.join(self.output_path, "returns")
        df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {df.count()} returns to {output_file}")
        return output_file
    
    def run(self):
        """Run all Bronze CSV processing"""
        print("Starting Bronze CSV processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_orders()
        self.process_line_items()
        self.process_returns()
        
        self.spark.stop()
        print("Bronze CSV processing complete!")