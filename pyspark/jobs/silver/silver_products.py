from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.utils.spark_utils import SparkUtils
from pyspark.utils.silver_utils import SilverUtils
import os


class SilverProductsJob:
    """Silver layer job for product data categorization and pricing"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("SilverProductsJob")
    
    def process_products(self):
        """Process and enrich product data"""
        print("Processing product data for Silver layer...")
        
        # Read Bronze product data
        products_df = self.spark.read.parquet(os.path.join(self.input_path, "products"))
        
        # Categorize products by price
        products_df = SilverUtils.categorize_price(products_df, "unit_price", "price_category")
        
        # Calculate profit margin
        products_df = products_df.withColumn(
            "profit_margin_pct",
            ((col("unit_price") - col("cost_price")) / col("unit_price")) * 100
        )
        
        # Add derived column: is_profitable
        products_df = products_df.withColumn(
            "is_profitable",
            when(col("profit_margin_pct") > 0, True).otherwise(False)
        )
        
        # Clean text fields
        products_df = SilverUtils.clean_text(products_df, "product_name")
        products_df = SilverUtils.clean_text(products_df, "brand")
        
        # Add date parts for launch date
        products_df = SilverUtils.add_date_parts(products_df, "launch_date")
        
        # Validate required columns
        required_columns = ["product_id", "product_name", "unit_price", "cost_price"]
        products_df = SilverUtils.validate_required_columns(products_df, required_columns)
        
        # Add audit columns
        products_df = SparkUtils.add_audit_columns(products_df, "silver_products")
        
        # Deduplicate
        products_df = SparkUtils.deduplicate(products_df, ["product_id"])
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "products")
        products_df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {products_df.count()} products to {output_file}")
        return output_file
    
    def run(self):
        """Run Silver product processing"""
        print("Starting Silver product processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_products()
        
        self.spark.stop()
        print("Silver product processing complete!")