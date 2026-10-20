from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count as _count, avg
from pyspark.utils.spark_utils import SparkUtils
from pyspark.utils.gold_utils import GoldUtils
import os


class GoldProductsJob:
    """Gold layer job for product analytics (sales, ranking)"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("GoldProductsJob")
    
    def process_product_analytics(self):
        """Process product analytics with sales ranking"""
        print("Processing product analytics...")
        
        # Read Silver sales data
        sales_df = self.spark.read.parquet(os.path.join(self.input_path, "sales"))
        
        # Aggregate by product
        product_stats = sales_df.groupBy("product_id").agg(
            _sum("line_item_total").alias("total_revenue"),
            _sum("quantity").alias("total_quantity_sold"),
            _count("order_id").alias("order_count"),
            avg("effective_price").alias("avg_price")
        )
        
        # Rank products by revenue
        product_stats = GoldUtils.rank_products(product_stats, "total_revenue", "revenue_rank")
        
        # Rank products by quantity sold
        product_stats = GoldUtils.rank_products(product_stats, "total_quantity_sold", "quantity_rank")
        
        # Add audit columns
        product_stats = SparkUtils.add_audit_columns(product_stats, "gold_products")
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "product_analytics")
        product_stats.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed product analytics to {output_file}")
        return output_file
    
    def run(self):
        """Run Gold product processing"""
        print("Starting Gold product processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_product_analytics()
        
        self.spark.stop()
        print("Gold product processing complete!")