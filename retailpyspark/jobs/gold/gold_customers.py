from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count as _count, avg, max as _max
from retailpyspark.utils.spark_utils import SparkUtils
from retailpyspark.utils.gold_utils import GoldUtils
import os


class GoldCustomersJob:
    """Gold layer job for customer analytics (RFM, lifetime value)"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("GoldCustomersJob")
    
    def process_customer_analytics(self):
        """Process customer analytics with RFM and lifetime value"""
        print("Processing customer analytics...")
        
        # Read Silver sales data
        sales_df = self.spark.read.parquet(os.path.join(self.input_path, "sales"))
        
        # Aggregate by customer
        customer_stats = sales_df.groupBy("customer_id").agg(
            _sum("total_amount").alias("total_revenue"),
            _count("order_id").alias("total_orders"),
            avg("total_amount").alias("avg_order_value"),
            _max("order_date").alias("last_purchase_date")
        )
        
        # Calculate customer lifetime value
        customer_stats = GoldUtils.calculate_customer_lifetime_value(
            customer_stats, "total_revenue", "order_id"
        )
        
        # Calculate RFM scores
        customer_stats = GoldUtils.calculate_rfm_scores(customer_stats)
        
        # Add customer segment based on lifetime value
        customer_stats = customer_stats.withColumn(
            "customer_segment",
            when(col("customer_lifetime_value") > 100000, "platinum")
            .when((col("customer_lifetime_value") >= 50000) & (col("customer_lifetime_value") <= 100000), "gold")
            .when((col("customer_lifetime_value") >= 10000) & (col("customer_lifetime_value") < 50000), "silver")
            .otherwise("bronze")
        )
        
        # Add audit columns
        customer_stats = SparkUtils.add_audit_columns(customer_stats, "gold_customers")
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "customer_analytics")
        customer_stats.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed customer analytics to {output_file}")
        return output_file
    
    def run(self):
        """Run Gold customer processing"""
        print("Starting Gold customer processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_customer_analytics()
        
        self.spark.stop()
        print("Gold customer processing complete!")
