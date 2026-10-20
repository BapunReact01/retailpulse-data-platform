from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count as _count, avg
from retailpyspark.utils.spark_utils import SparkUtils
from retailpyspark.utils.gold_utils import GoldUtils
import os


class GoldStoresJob:
    """Gold layer job for store analytics (performance metrics)"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("GoldStoresJob")
    
    def process_store_analytics(self):
        """Process store analytics with performance metrics"""
        print("Processing store analytics...")
        
        # Read Silver sales data
        sales_df = self.spark.read.parquet(os.path.join(self.input_path, "sales"))
        
        # Aggregate by store
        store_stats = sales_df.groupBy("store_id").agg(
            _sum("total_amount").alias("total_revenue"),
            _count("order_id").alias("total_orders"),
            _count("customer_id").alias("unique_customers"),
            avg("total_amount").alias("avg_order_value")
        )
        
        # Calculate revenue per customer
        store_stats = store_stats.withColumn(
            "revenue_per_customer",
            col("total_revenue") / col("unique_customers")
        )
        
        # Rank stores by revenue
        store_stats = GoldUtils.rank_products(store_stats, "total_revenue", "revenue_rank")
        
        # Add audit columns
        store_stats = SparkUtils.add_audit_columns(store_stats, "gold_stores")
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "store_analytics")
        store_stats.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed store analytics to {output_file}")
        return output_file
    
    def run(self):
        """Run Gold store processing"""
        print("Starting Gold store processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_store_analytics()
        
        self.spark.stop()
        print("Gold store processing complete!")
