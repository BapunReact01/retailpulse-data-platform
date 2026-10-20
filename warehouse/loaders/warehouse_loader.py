import psycopg2
from typing import Dict, Any, List


class WarehouseLoader:
    """Base class for warehouse loading operations"""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print(f"Connected to warehouse database: {self.database}")
            return True
        except Exception as e:
            print(f"Error connecting to warehouse: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("Disconnected from warehouse database")
    
    def execute_sql(self, sql: str):
        """Execute SQL statement"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            print(f"SQL executed successfully")
            return True
        except Exception as e:
            print(f"Error executing SQL: {e}")
            self.conn.rollback()
            return False
    
    def execute_many(self, sql: str, data: List[tuple]):
        """Execute SQL with multiple rows"""
        try:
            cursor = self.conn.cursor()
            cursor.executemany(sql, data)
            self.conn.commit()
            print(f"Inserted {len(data)} rows")
            return True
        except Exception as e:
            print(f"Error executing batch insert: {e}")
            self.conn.rollback()
            return False
    
    def execute_file(self, file_path: str):
        """Execute SQL from file"""
        try:
            with open(file_path, 'r') as f:
                sql = f.read()
                cursor = self.conn.cursor()
                cursor.execute(sql)
                self.conn.commit()
            print(f"Executed SQL from {file_path}")
            return True
        except Exception as e:
            print(f"Error executing SQL file: {e}")
            self.conn.rollback()
            return False