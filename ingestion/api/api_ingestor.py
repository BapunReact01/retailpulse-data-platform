import requests
from typing import List, Dict, Any
from ingestion.base.base_ingestor import BaseIngestor


class APIIngestor(BaseIngestor):
    """Ingestor for REST API data sources"""
    
    def __init__(self, base_url: str, source_name: str, output_path: str):
        super().__init__(source_name, output_path)
        self.base_url = base_url
        self.timeout = 30
    
    def extract(self) -> List[Dict[str, Any]]:
        """Extract data from API endpoint"""
        try:
            response = requests.get(
                self.base_url,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            # Handle different response structures
            if isinstance(data, dict) and 'data' in data:
                return data['data']
            elif isinstance(data, list):
                return data
            else:
                return [data]
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {self.base_url}: {e}")
            return []
    
    def extract_endpoint(self, endpoint: str) -> List[Dict[str, Any]]:
        """Extract data from a specific endpoint"""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            if isinstance(data, dict) and 'data' in data:
                return data['data']
            elif isinstance(data, list):
                return data
            else:
                return [data]
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
            return []