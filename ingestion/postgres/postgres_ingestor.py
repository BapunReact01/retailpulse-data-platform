import psycopg2
from typing import List, Dict, Any
from ingestion.base.base_ingestor import BaseIngestor


class PostgresIngestor(BaseIngestor):
    """Ingestor for PostgreSQL database data sources"""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str, 
                 source_name: str, output_path: str):
        super().__init__(source_name, output_path)
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
    
    def extract(self) -> List[Dict[str, Any]]:
        """Extract data from all tables (not recommended, use extract_table instead)"""
        return []
    
    def extract_table(self, table_name: str, query: str = None) -> List[Dict[str, Any]]:
        """Extract data from a specific table"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            
            if query:
                sql = query
            else:
                sql = f"SELECT * FROM {table_name}"
            
            cursor.execute(sql)
            
            # Get column names
            column_names = [desc[0] for desc in cursor.description]
            
            # Fetch all rows
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            data = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                data.append(row_dict)
            
            cursor.close()
            conn.close()
            
            print(f"Extracted {len(data)} records from table {table_name}")
            return data
            
        except Exception as e:
            print(f"Error extracting from {table_name}: {e}")
            return []
    
    def extract_query(self, query: str) -> List[Dict[str, Any]]:
        """Extract data using a custom SQL query"""
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            
            cursor.execute(query)
            
            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            
            data = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                data.append(row_dict)
            
            cursor.close()
            conn.close()
            
            print(f"Extracted {len(data)} records using custom query")
            return data
            
        except Exception as e:
            print(f"Error executing query: {e}")
            return []