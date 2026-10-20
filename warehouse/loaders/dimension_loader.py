from .warehouse_loader import WarehouseLoader
from typing import List, Dict, Any
import psycopg2.extras


class DimensionLoader(WarehouseLoader):
    """Loader for dimension tables"""
    
    def load_customers(self, customers_data: List[Dict[str, Any]]):
        """Load customer dimension"""
        sql = """
            INSERT INTO dim_customers (
                customer_id, first_name, last_name, email, phone, city, state,
                country, postal_code, registration_date, customer_segment,
                customer_tier, loyalty_score, days_as_customer, customer_lifetime_value
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (customer_id) DO UPDATE SET
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                email = EXCLUDED.email,
                phone = EXCLUDED.phone,
                city = EXCLUDED.city,
                state = EXCLUDED.state,
                country = EXCLUDED.country,
                postal_code = EXCLUDED.postal_code,
                customer_segment = EXCLUDED.customer_segment,
                customer_tier = EXCLUDED.customer_tier,
                loyalty_score = EXCLUDED.loyalty_score,
                days_as_customer = EXCLUDED.days_as_customer,
                customer_lifetime_value = EXCLUDED.customer_lifetime_value,
                expiry_date = CURRENT_DATE
        """
        
        data = [
            (
                c['customer_id'], c['first_name'], c['last_name'], c['email'],
                c.get('phone'), c.get('city'), c.get('state'), c.get('country', 'India'),
                c.get('postal_code'), c['registration_date'], c.get('customer_segment'),
                c.get('customer_tier'), c.get('loyalty_score'), c.get('days_as_customer'),
                c.get('customer_lifetime_value')
            )
            for c in customers_data
        ]
        
        return self.execute_many(sql, data)
    
    def load_products(self, products_data: List[Dict[str, Any]]):
        """Load product dimension"""
        sql = """
            INSERT INTO dim_products (
                product_id, product_name, category, subcategory, brand,
                unit_price, cost_price, launch_date, is_active, price_category,
                profit_margin_pct, is_profitable
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (product_id) DO UPDATE SET
                product_name = EXCLUDED.product_name,
                category = EXCLUDED.category,
                subcategory = EXCLUDED.subcategory,
                brand = EXCLUDED.brand,
                unit_price = EXCLUDED.unit_price,
                cost_price = EXCLUDED.cost_price,
                is_active = EXCLUDED.is_active,
                price_category = EXCLUDED.price_category,
                profit_margin_pct = EXCLUDED.profit_margin_pct,
                is_profitable = EXCLUDED.is_profitable,
                expiry_date = CURRENT_DATE
        """
        
        data = [
            (
                p['product_id'], p['product_name'], p['category'], p.get('subcategory'),
                p.get('brand'), p['unit_price'], p['cost_price'], p.get('launch_date'),
                p.get('is_active', True), p.get('price_category'), p.get('profit_margin_pct'),
                p.get('is_profitable')
            )
            for p in products_data
        ]
        
        return self.execute_many(sql, data)
    
    def load_stores(self, stores_data: List[Dict[str, Any]]):
        """Load store dimension"""
        sql = """
            INSERT INTO dim_stores (
                store_id, store_name, city, state, country, store_type,
                opening_date, manager_name, store_size_sqft
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (store_id) DO UPDATE SET
                store_name = EXCLUDED.store_name,
                city = EXCLUDED.city,
                state = EXCLUDED.state,
                country = EXCLUDED.country,
                store_type = EXCLUDED.store_type,
                manager_name = EXCLUDED.manager_name,
                store_size_sqft = EXCLUDED.store_size_sqft,
                expiry_date = CURRENT_DATE
        """
        
        data = [
            (
                s['store_id'], s['store_name'], s['city'], s.get('state'),
                s.get('country', 'India'), s.get('store_type'), s.get('opening_date'),
                s.get('manager_name'), s.get('store_size_sqft')
            )
            for s in stores_data
        ]
        
        return self.execute_many(sql, data)
    
    def load_dates(self, dates_data: List[Dict[str, Any]]):
        """Load date dimension"""
        sql = """
            INSERT INTO dim_dates (
                date_key, date_value, day_of_week, day_of_month, day_of_year,
                week_of_year, month, quarter, year, is_holiday, is_weekend,
                month_name, day_name
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (date_value) DO NOTHING
        """
        
        data = [
            (
                d['date_key'], d['date_value'], d['day_of_week'], d['day_of_month'],
                d['day_of_year'], d['week_of_year'], d['month'], d['quarter'],
                d['year'], d.get('is_holiday', False), d.get('is_weekend', False),
                d['month_name'], d['day_name']
            )
            for d in dates_data
        ]
        
        return self.execute_many(sql, data)