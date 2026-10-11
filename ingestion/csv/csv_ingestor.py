import csv
import os
from typing import List, Dict, Any
from ingestion.base.base_ingestor import BaseIngestor


class CSVIngestor(BaseIngestor):
    """Ingestor for CSV file data sources"""
    
    def __init__(self, source_path: str, source_name: str, output_path: str):
        super().__init__(source_name, output_path)
        self.source_path = source_path
    
    def extract(self) -> List[Dict[str, Any]]:
        """Extract data from CSV file"""
        if not os.path.exists(self.source_path):
            print(f"CSV file not found: {self.source_path}")
            return []
        
        data = []
        try:
            with open(self.source_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert empty strings to None for proper JSON serialization
                    cleaned_row = {k: (v if v else None) for k, v in row.items()}
                    data.append(cleaned_row)
                    
        except Exception as e:
            print(f"Error reading CSV file {self.source_path}: {e}")
            return []
        
        return data
    
    def extract_directory(self, directory: str, pattern: str = "*.csv") -> List[Dict[str, Any]]:
        """Extract data from all CSV files in a directory"""
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return []
        
        all_data = []
        try:
            for filename in os.listdir(directory):
                if filename.endswith('.csv'):
                    filepath = os.path.join(directory, filename)
                    file_data = self._extract_file(filepath)
                    all_data.extend(file_data)
                    
        except Exception as e:
            print(f"Error reading directory {directory}: {e}")
            return []
        
        return all_data
    
    def _extract_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Extract data from a single CSV file"""
        data = []
        try:
            with open(filepath, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned_row = {k: (v if v else None) for k, v in row.items()}
                    data.append(cleaned_row)
                    
        except Exception as e:
            print(f"Error reading CSV file {filepath}: {e}")
            return []
        
        return data