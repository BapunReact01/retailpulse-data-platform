from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit
from pyspark.sql.types import StructType, StringType, TimestampType
import uuid


class SparkUtils:
    """Utility class for common PySpark operations"""
    
    @staticmethod
    def get_spark_session(app_name: str = "RetailPulse") -> SparkSession:
        """Create and return a SparkSession"""
        return SparkSession.builder \
            .appName(app_name) \
            .config("spark.sql.shuffle.partitions", "4") \
            .config("spark.sql.legacy.timeParserPolicy", "LEGACY") \
            .getOrCreate()
    
    @staticmethod
    def add_audit_columns(df, source: str):
        """Add audit columns to DataFrame"""
        return df.withColumn("ingestion_time", current_timestamp()) \
                 .withColumn("source", lit(source)) \
                 .withColumn("record_id", lit(str(uuid.uuid4())))
    
    @staticmethod
    def handle_nulls(df, columns_to_check=None):
        """Handle null values in specified columns"""
        if columns_to_check:
            for col_name in columns_to_check:
                df = df.fillna({col_name: "unknown"})
        return df
    
    @staticmethod
    def deduplicate(df, key_columns):
        """Remove duplicate records based on key columns"""
        return df.dropDuplicates(key_columns)
    
    @staticmethod
    def cast_types(df, type_mapping):
        """Cast columns to specified types"""
        for col_name, data_type in type_mapping.items():
            df = df.withColumn(col_name, col(col_name).cast(data_type))
        return df