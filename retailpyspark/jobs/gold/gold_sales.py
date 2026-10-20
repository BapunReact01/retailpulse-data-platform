from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, count as _count, avg, year, month, dayofmonth
from retailpyspark.utils.spark_utils import SparkUtils
from retailpyspark.utils.gold_utils import GoldUtils
import os


class GoldSalesJob:
    """Gold layer job for sales aggregations and KPIs"""
    
    def __init__(self, input_path: str, output_path: str):
        self.input_path = input_path
        self.output_path = output_path
        self.spark = SparkUtils.get_spark_session("GoldSalesJob")
    
    def process_daily_sales(self):
        """Process daily sales aggregations"""
        print("Processing daily sales aggregations...")
        
        # Read Silver sales data
        sales_df = self.spark.read.parquet(os.path.join(self.input_path, "sales"))
        
        # Aggregate by date
        daily_sales = sales_df.groupBy("order_date_year", "order_date_month", "order_date_day").agg(
            _sum("total_amount").alias("daily_revenue"),
            _count("order_id").alias("daily_orders"),
            _count("customer_id").alias("daily_customers"),
            avg("total_amount").alias("avg_order_value")
        )
        
        # Add audit columns
        daily_sales = SparkUtils.add_audit_columns(daily_sales, "gold_daily_sales")
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "daily_sales")
        daily_sales.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed daily sales to {output_file}")
        return output_file
    
    def process_kpis(self):
        """Process overall KPIs"""
        print("Processing overall KPIs...")
        
        # Read Silver sales data
        sales_df = self.spark.read.parquet(os.path.join(self.input_path, "sales"))
        
        # Calculate KPIs
        total_revenue = GoldUtils.calculate_total_revenue(sales_df)
        avg_order_value = GoldUtils.calculate_average_order_value(sales_df)
        total_orders = GoldUtils.calculate_total_orders(sales_df)
        
        # Combine KPIs into a single row
        kpis = total_revenue.crossJoin(avg_order_value).crossJoin(total_orders)
        
        # Add audit columns
        kpis = SparkUtils.add_audit_columns(kpis, "gold_kpis")
        
        # Write to Parquet
        output_file = os.path.join(self.output_path, "kpis")
        kpis.write.mode("overwrite").parquet(output_file)
        
        print(f"Processed KPIs to {output_file}")
        return output_file
    
    def run(self):
        """Run Gold sales processing"""
        print("Starting Gold sales processing...")
        
        os.makedirs(self.output_path, exist_ok=True)
        
        self.process_daily_sales()
        self.process_kpis()
        
        self.spark.stop()
        print("Gold sales processing complete!")
