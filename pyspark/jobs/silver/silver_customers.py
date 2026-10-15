from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, concat_ws, lit
from pyspark.utils.spark_utils import SparkUtils
from pyspark.utils.silver_utils import SilverUtils
import os


class SilverCustomersJob:
    """Silver layer job for customer data enrichment and standardization"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("SilverCustomersJob")
    
    def process_customers(self):
        """Process and enrich customer data"""
        print("Processing customer data for Silver layer...")
        
        # Read Bronze customer data
        customers_df = self.spark.read.parquet(os.path.join(self.input_path, "customers"))
        
        # Standardize email and phone
        customers_df = SilverUtils.standardize_email(customers_df, "email")
        customers_df = SilverUtils.standardize_phone(customers_df, "phone")
        
        # Standardize address
        customers_df = SilverUtils.standardize_address(customers_df, "street", "city")
        
        # Clean text fields
        customers_df = SilverUtils.clean_text(customers_df, "first_name")
        customers_df = SilverUtils.clean_text(customers_df, "last_name")
        
        # Calculate customer tenure (days since registration)
        customers_df = SilverUtils.calculate_days_since(customers_df, "registration_date", "days_as_customer")
        
        # Add derived column: full name
        customers_df = customers_df.withColumn(
            "full_name",
            concat_ws(" ", col("first_name"), col("last_name"))
        )
        
        # Add derived column: loyalty score based on segment and tier
        customers_df = customers_df.withColumn(
            "loyalty_score",
            when(col("customer_segment") == "premium", 100)
            .when(col("customer_segment") == "regular", 50)
            .when(col("customer_segment") == "new", 25)
            .otherwise(0)
        )
        
        # Validate required columns
        required_columns = ["customer_id", "email", "first_name", "last_name"]
        customers_df = SilverUtils.validate_required_columns(customers_df, required_columns)
        
        # Add audit columns
        customers_df = SparkUtils.add_audit_columns(customers_df, "silver_customers")
        
        # Deduplicate
        customers_df = SparkUtils.deduplicate(customers_df, ["customer_id"])
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "customers")
        customers_df.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed {customers_df.count()} customers to {output_file}")
        return output_file
    
    def run(self):
        """Run Silver customer processing"""
        print("Starting Silver customer processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_customers()
        
        self.spark.stop()
        print("Silver customer processing complete!")