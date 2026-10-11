from abc import ABC, abstractmethod
from datetime import datetime
import json
import os
from typing import List, Dict, Any


class BaseIngestor(ABC):
    """Base class for all data ingestors"""
    
    def __init__(self, source_name: str, output_path: str):
        self.source_name = source_name
        self.output_path = output_path
        self.ingestion_timestamp = datetime.now()
    
    @abstractmethod
    def extract(self) -> List[Dict[str, Any]]:
        """Extract data from the source"""
        pass
    
    def save_to_json(self, data: List[Dict[str, Any]], filename: str):
        """Save data to JSON file"""
        os.makedirs(self.output_path, exist_ok=True)
        filepath = os.path.join(self.output_path, filename)
        
        output_data = {
            'source': self.source_name,
            'ingestion_timestamp': self.ingestion_timestamp.isoformat(),
            'record_count': len(data),
            'data': data
        }
        
        with open(filepath, 'w') as f:
            json.dump(output_data, f, indent=2, default=str)
        
        print(f"Saved {len(data)} records to {filepath}")
        return filepath
    
    def save_to_csv(self, data: List[Dict[str, Any]], filename: str):
        """Save data to CSV file"""
        import csv
        
        os.makedirs(self.output_path, exist_ok=True)
        filepath = os.path.join(self.output_path, filename)
        
        if not data:
            print(f"No data to save to {filepath}")
            return filepath
        
        fieldnames = data[0].keys()
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Saved {len(data)} records to {filepath}")
        return filepath
    
    def ingest(self, format: str = 'json') -> str:
        """Main ingestion method"""
        print(f"Starting ingestion from {self.source_name}...")
        
        data = self.extract()
        print(f"Extracted {len(data)} records")
        
        timestamp = self.ingestion_timestamp.strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = f"{self.source_name}_{timestamp}.json"
            filepath = self.save_to_json(data, filename)
        elif format == 'csv':
            filename = f"{self.source_name}_{timestamp}.csv"
            filepath = self.save_to_csv(data, filename)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        print(f"Ingestion complete: {filepath}")
        return filepath