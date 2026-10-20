from pyspark.sql import DataFrame
from pyspark.sql.functions import col, when, upper, lower, trim, regexp_replace, coalesce
from pyspark.sql.functions import datediff, current_date, year, month, dayofmonth
from datetime import datetime


class SilverUtils:
    """Utility class for Silver layer transformations"""
    
    @staticmethod
    def standardize_email(df, email_col="email"):
        """Standardize email addresses"""
        return df.withColumn(email_col, lower(trim(col(email_col))))
    
    @staticmethod
    def standardize_phone(df, phone_col="phone"):
        """Standardize phone numbers - remove special characters"""
        return df.withColumn(phone_col, regexp_replace(col(phone_col), "[^0-9+]", ""))
    
    @staticmethod
    def standardize_address(df, street_col="street", city_col="city"):
        """Standardize address fields"""
        df = df.withColumn(street_col, trim(col(street_col)))
        df = df.withColumn(city_col, upper(trim(col(city_col))))
        return df
    
    @staticmethod
    def calculate_age(df, date_col, age_col="age"):
        """Calculate age from date of birth"""
        return df.withColumn(age_col, datediff(current_date(), col(date_col)) / 365)
    
    @staticmethod
    def calculate_days_since(df, date_col, days_col="days_since"):
        """Calculate days since a given date"""
        return df.withColumn(days_col, datediff(current_date(), col(date_col)))
    
    @staticmethod
    def categorize_price(df, price_col, category_col="price_category"):
        """Categorize prices into ranges"""
        return df.withColumn(category_col, 
            when(col(price_col) < 1000, "low")
            .when((col(price_col) >= 1000) & (col(price_col) < 5000), "medium")
            .when((col(price_col) >= 5000) & (col(price_col) < 10000), "high")
            .otherwise("premium")
        )
    
    @staticmethod
    def calculate_discount_pct(df, unit_price_col, discount_col, discount_pct_col="discount_pct"):
        """Calculate discount percentage"""
        return df.withColumn(discount_pct_col, 
            (col(discount_col) / col(unit_price_col)) * 100
        )
    
    @staticmethod
    def add_date_parts(df, date_col):
        """Add year, month, day columns from date"""
        df = df.withColumn(f"{date_col}_year", year(col(date_col)))
        df = df.withColumn(f"{date_col}_month", month(col(date_col)))
        df = df.withColumn(f"{date_col}_day", dayofmonth(col(date_col)))
        return df
    
    @staticmethod
    def clean_text(df, text_col):
        """Clean text fields - remove extra spaces"""
        return df.withColumn(text_col, trim(regexp_replace(col(text_col), "\\s+", " ")))
    
    @staticmethod
    def validate_required_columns(df, required_columns):
        """Check if required columns exist and have non-null values"""
        for col_name in required_columns:
            null_count = df.filter(col(col_name).isNull()).count()
            if null_count > 0:
                print(f"Warning: {null_count} null values found in column {col_name}")
        return df