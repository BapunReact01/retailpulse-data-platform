from .warehouse_loader import WarehouseLoader
from typing import List, Dict, Any


class FactLoader(WarehouseLoader):
    """Loader for fact tables"""
    
    def load_sales(self, sales_data: List[Dict[str, Any]]):
        """Load sales fact table"""
        sql = """
            INSERT INTO fact_sales (
                order_id, customer_key, product_key, store_key, date_key,
                line_item_id, quantity, unit_price, discount, line_item_total,
                effective_price, total_amount, order_value_category, payment_method, source
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (sales_key) DO NOTHING
        """
        
        data = [
            (
                s['order_id'], s['customer_key'], s['product_key'], s['store_key'],
                s['date_key'], s['line_item_id'], s['quantity'], s['unit_price'],
                s.get('discount', 0), s['line_item_total'], s.get('effective_price'),
                s['total_amount'], s.get('order_value_category'), s.get('payment_method'),
                s.get('source', 'silver_sales')
            )
            for s in sales_data
        ]
        
        return self.execute_many(sql, data)
    
    def load_returns(self, returns_data: List[Dict[str, Any]]):
        """Load returns fact table"""
        sql = """
            INSERT INTO fact_returns (
                return_id, customer_key, product_key, store_key, date_key,
                return_date, reason, refund_amount, status, source
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            ON CONFLICT (return_id) DO NOTHING
        """
        
        data = [
            (
                r['return_id'], r['customer_key'], r['product_key'], r['store_key'],
                r['date_key'], r['return_date'], r.get('reason'), r['refund_amount'],
                r.get('status', 'pending'), r.get('source', 'raw_returns')
            )
            for r in returns_data
        ]
        
        return self.execute_many(sql, data)
    
    def get_dimension_key(self, table: str, id_column: str, id_value: str) -> int:
        """Get surrogate key from dimension table"""
        sql = f"SELECT customer_key FROM {table} WHERE {id_column} = %s"
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_value,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"Error getting dimension key: {e}")
            return None