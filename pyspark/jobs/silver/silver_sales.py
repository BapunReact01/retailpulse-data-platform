from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, sum as _sum, count as _count, avg
from pyspark.utils.spark_utils import SparkUtils
from pyspark.utils.silver_utils import SilverUtils
import os


class SilverSalesJob:
    """Silver layer job for sales data with joins and aggregations"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("SilverSalesJob")
    
    def process_sales(self):
        """Process and enrich sales data by joining orders and line items"""
        print("Processing sales data for Silver layer...")
        
        # Read Bronze data
        orders_df = self.spark.read.parquet(os.path.join(self.input_path, "orders"))
        line_items_df = self.spark.read.parquet(os.path.join(self.input_path, "line_items"))
        
        # Join orders with line items
        sales_df = orders_df.join(
            line_items_df,
            on="order_id",
            how="inner"
        )
        
        # Calculate line item total
        sales_df = sales_df.withColumn(
            "line_item_total",
            (col("quantity") * col("unit_price")) - col("discount")
        )
        
        # Calculate effective price after discount
        sales_df = sales_df.withColumn(
            "effective_price",
            col("unit_price") - (col("discount") / col("quantity"))
        )
        
        # Add date parts for order date
        sales_df = SilverUtils.add_date_parts(sales_df, "order_date")
        
        # Categorize order value
        sales_df = sales_df.withColumn(
            "order_value_category",
            when(col("total_amount") < 1000, "small")
            .when((col("total_amount") >= 1000) & (col("total_amount") < 5000), "medium")
            .when((col("total_amount") >= 5000) & (col("total_amount") < 10000), "large")
            .otherwise("enterprise")
        )
        
        # Validate required columns
        required_columns = ["order_id", "customer_id", "store_id", "product_id"]
        sales_df = SilverUtils.validate_required_columns(sales_df, required_columns)
        
        # Add audit columns
        sales_df = SparkUtils.add_audit_columns(sales_df, "silver_sales")
        
        # Deduplicate on line_item_id
        sales_df = SparkUtils.deduplicate(sales_df, ["line_item_id"])
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "sales")
        sales_df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {sales_df.count()} sales records to {output_file}")
        return output_file
    
    def run(self):
        """Run Silver sales processing"""
        print("Starting Silver sales processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_sales()
        
        self.spark.stop()
        print("Silver sales processing complete!")
