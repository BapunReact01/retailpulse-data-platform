import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, current_timestamp, to_date
from pyspark.sql.types import *

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def create_spark_session():
    """Create Spark session with Windows fix"""
    spark = SparkSession.builder \
        .appName("RetailPulse_LargeDatasetLoader") \
        .config("spark.hadoop.hadoop.native.lib", "false") \
        .config("spark.sql.warehouse.dir", "file:///C:/Users/Bapun/myproject/retailpulse-data-platform/data") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    return spark

def load_and_transform_customers(spark, input_path, output_path):
    """Load and transform customers data"""
    print("Loading customers data...")
    
    df = spark.read.parquet(f"{input_path}/customers.parquet")
    
    # Show schema
    print("Customers schema:")
    df.printSchema()
    
    # Show sample data
    print("Sample customers data:")
    df.show(5)
    
    # Transform to match your schema (adjust column names as needed)
    # This is a placeholder - you'll need to map actual columns
    df_transformed = df.withColumn("ingestion_time", current_timestamp())
    
    # Save to raw layer
    df_transformed.write.mode("overwrite").parquet(f"{output_path}/customers")
    print(f"✅ Customers saved to {output_path}/customers")
    
    return df_transformed

def load_and_transform_products(spark, input_path, output_path):
    """Load and transform products data"""
    print("Loading products data...")
    
    df = spark.read.parquet(f"{input_path}/products.parquet")
    
    print("Products schema:")
    df.printSchema()
    
    print("Sample products data:")
    df.show(5)
    
    df_transformed = df.withColumn("ingestion_time", current_timestamp())
    
    df_transformed.write.mode("overwrite").parquet(f"{output_path}/products")
    print(f"✅ Products saved to {output_path}/products")
    
    return df_transformed

def load_and_transform_orders(spark, input_path, output_path):
    """Load and transform orders data"""
    print("Loading orders data...")
    
    df = spark.read.parquet(f"{input_path}/orders.parquet")
    
    print("Orders schema:")
    df.printSchema()
    
    print("Sample orders data:")
    df.show(5)
    
    df_transformed = df.withColumn("ingestion_time", current_timestamp())
    
    df_transformed.write.mode("overwrite").parquet(f"{output_path}/orders")
    print(f"✅ Orders saved to {output_path}/orders")
    
    return df_transformed

def load_and_transform_order_items(spark, input_path, output_path):
    """Load and transform order items data"""
    print("Loading order items data...")
    
    df = spark.read.parquet(f"{input_path}/order_items.parquet")
    
    print("Order items schema:")
    df.printSchema()
    
    print("Sample order items data:")
    df.show(5)
    
    df_transformed = df.withColumn("ingestion_time", current_timestamp())
    
    df_transformed.write.mode("overwrite").parquet(f"{output_path}/order_items")
    print(f"✅ Order items saved to {output_path}/order_items")
    
    return df_transformed

def main():
    """Main function to load all data"""
    spark = create_spark_session()
    
    input_path = "data/large_dataset"
    output_path = "data/raw/large_dataset"
    
    os.makedirs(output_path, exist_ok=True)
    
    print("=" * 60)
    print("Loading FreeEcommerceTwin14M Dataset")
    print("=" * 60)
    
    # Load each dataset
    try:
        load_and_transform_customers(spark, input_path, output_path)
        load_and_transform_products(spark, input_path, output_path)
        load_and_transform_orders(spark, input_path, output_path)
        load_and_transform_order_items(spark, input_path, output_path)
        
        print("=" * 60)
        print("✅ All data loaded successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
    
    spark.stop()

if __name__ == "__main__":
    main()