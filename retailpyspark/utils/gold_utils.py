from pyspark.sql import DataFrame
from pyspark.sql.functions import col, sum as _sum, count as _count, avg, max as _max, min as _min
from pyspark.sql.functions import datediff, current_date, when, row_number
from pyspark.sql.window import Window


class GoldUtils:
    """Utility class for Gold layer aggregations and KPIs"""
    
    @staticmethod
    def calculate_total_revenue(df, revenue_col="total_amount"):
        """Calculate total revenue"""
        return df.agg(_sum(revenue_col).alias("total_revenue"))
    
    @staticmethod
    def calculate_average_order_value(df, revenue_col="total_amount"):
        """Calculate average order value"""
        return df.agg(avg(revenue_col).alias("avg_order_value"))
    
    @staticmethod
    def calculate_total_orders(df, order_col="order_id"):
        """Calculate total number of orders"""
        return df.agg(_count(order_col).alias("total_orders"))
    
    @staticmethod
    def calculate_profit(df, unit_price_col, cost_price_col, quantity_col="quantity"):
        """Calculate total profit"""
        return df.withColumn(
            "profit",
            (col(unit_price_col) - col(cost_price_col)) * col(quantity_col)
        )
    
    @staticmethod
    def calculate_profit_margin(df, revenue_col, profit_col):
        """Calculate profit margin percentage"""
        return df.withColumn(
            "profit_margin_pct",
            (col(profit_col) / col(revenue_col)) * 100
        )
    
    @staticmethod
    def rank_products(df, metric_col, rank_col="rank"):
        """Rank products by a metric (e.g., sales, revenue)"""
        window_spec = Window.orderBy(col(metric_col).desc())
        return df.withColumn(rank_col, row_number().over(window_spec))
    
    @staticmethod
    def add_ranking(df, partition_cols, order_cols, rank_col="rank"):
        """Add ranking column with partitioning"""
        window_spec = Window.partitionBy(*partition_cols).orderBy(*order_cols)
        return df.withColumn(rank_col, row_number().over(window_spec))
    
    @staticmethod
    def calculate_customer_lifetime_value(df, revenue_col, order_col="order_id"):
        """Calculate customer lifetime value"""
        return df.groupBy("customer_id").agg(
            _sum(revenue_col).alias("total_revenue"),
            _count(order_col).alias("total_orders"),
            avg(revenue_col).alias("avg_order_value")
        ).withColumn(
            "customer_lifetime_value",
            col("total_revenue") * col("total_orders")
        )
    
    @staticmethod
    def calculate_rfm_scores(df):
        """Calculate RFM (Recency, Frequency, Monetary) scores for customers"""
        # Recency: days since last purchase
        df = df.withColumn(
            "recency_days",
            datediff(current_date(), col("last_purchase_date"))
        )
        
        # Frequency: number of purchases
        df = df.withColumn("frequency", col("total_orders"))
        
        # Monetary: total spent
        df = df.withColumn("monetary", col("total_revenue"))
        
        return df