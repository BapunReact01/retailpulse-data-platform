import json
import os
from typing import List, Dict, Any
from datetime import datetime


class QuarantineHandler:
    """Handler for quarantining invalid records"""
    
    def __init__(self, quarantine_dir: str = "data/quarantine"):
        self.quarantine_dir = quarantine_dir
        os.makedirs(quarantine_dir, exist_ok=True)
    
    def quarantine_records(self, records: List[Dict], source: str, reason: str) -> str:
        """Save invalid records to quarantine"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{source}_quarantine_{timestamp}.json"
        filepath = os.path.join(self.quarantine_dir, filename)
        
        quarantine_data = {
            'source': source,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'record_count': len(records),
            'records': records
        }
        
        with open(filepath, 'w') as f:
            json.dump(quarantine_data, f, indent=2, default=str)
        
        print(f"Quarantined {len(records)} records to {filepath}")
        return filepath
    
    def get_quarantine_stats(self) -> Dict[str, Any]:
        """Get statistics about quarantined records"""
        quarantine_files = [f for f in os.listdir(self.quarantine_dir) if f.endswith('.json')]
        
        total_records = 0
        files_by_source = {}
        
        for file in quarantine_files:
            filepath = os.path.join(self.quarantine_dir, file)
            with open(filepath, 'r') as f:
                data = json.load(f)
                total_records += data.get('record_count', 0)
                source = data.get('source', 'unknown')
                files_by_source[source] = files_by_source.get(source, 0) + 1
        
        return {
            'total_quarantine_files': len(quarantine_files),
            'total_quarantined_records': total_records,
            'files_by_source': files_by_source
        }