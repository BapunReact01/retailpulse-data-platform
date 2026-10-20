from typing import List, Dict, Any, Tuple
from datetime import datetime


class DataValidator:
    """Data quality validator for checking data rules"""
    
    def __init__(self):
        self.violations = []
        self.total_records = 0
        self.valid_records = 0
        self.invalid_records = 0
    
    def validate_not_null(self, data: List[Dict], columns: List[str]) -> Tuple[bool, List[Dict]]:
        """Check that specified columns are not null"""
        invalid_records = []
        
        for idx, record in enumerate(data):
            self.total_records += 1
            for col in columns:
                if col not in record or record[col] is None or record[col] == '':
                    self.violations.append({
                        'rule': 'NOT_NULL',
                        'column': col,
                        'record_id': idx,
                        'message': f"Column '{col}' is null or empty"
                    })
                    invalid_records.append(record)
                    self.invalid_records += 1
                    break
            else:
                self.valid_records += 1
        
        return len(invalid_records) == 0, invalid_records
    
    def validate_data_type(self, data: List[Dict], column: str, expected_type: type) -> Tuple[bool, List[Dict]]:
        """Check that column values match expected type"""
        invalid_records = []
        
        for idx, record in enumerate(data):
            if column in record and record[column] is not None:
                if not isinstance(record[column], expected_type):
                    self.violations.append({
                        'rule': 'DATA_TYPE',
                        'column': column,
                        'record_id': idx,
                        'message': f"Column '{column}' should be {expected_type.__name__}, got {type(record[column]).__name__}"
                    })
                    invalid_records.append(record)
                    self.invalid_records += 1
        
        return len(invalid_records) == 0, invalid_records
    
    def validate_range(self, data: List[Dict], column: str, min_val: Any, max_val: Any) -> Tuple[bool, List[Dict]]:
        """Check that column values are within range"""
        invalid_records = []
        
        for idx, record in enumerate(data):
            if column in record and record[column] is not None:
                if not (min_val <= record[column] <= max_val):
                    self.violations.append({
                        'rule': 'RANGE',
                        'column': column,
                        'record_id': idx,
                        'message': f"Column '{column}' value {record[column]} is outside range [{min_val}, {max_val}]"
                    })
                    invalid_records.append(record)
                    self.invalid_records += 1
        
        return len(invalid_records) == 0, invalid_records
    
    def validate_uniqueness(self, data: List[Dict], column: str) -> Tuple[bool, List[Dict]]:
        """Check that column values are unique"""
        invalid_records = []
        seen_values = {}
        
        for idx, record in enumerate(data):
            if column in record and record[column] is not None:
                value = record[column]
                if value in seen_values:
                    self.violations.append({
                        'rule': 'UNIQUENESS',
                        'column': column,
                        'record_id': idx,
                        'message': f"Duplicate value '{value}' in column '{column}'"
                    })
                    invalid_records.append(record)
                    self.invalid_records += 1
                else:
                    seen_values[value] = idx
        
        return len(invalid_records) == 0, invalid_records
    
    def validate_email_format(self, data: List[Dict], column: str) -> Tuple[bool, List[Dict]]:
        """Check that email column has valid format"""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_records = []
        
        for idx, record in enumerate(data):
            if column in record and record[column] is not None:
                if not re.match(email_pattern, record[column]):
                    self.violations.append({
                        'rule': 'EMAIL_FORMAT',
                        'column': column,
                        'record_id': idx,
                        'message': f"Invalid email format: {record[column]}"
                    })
                    invalid_records.append(record)
                    self.invalid_records += 1
        
        return len(invalid_records) == 0, invalid_records
    
    def validate_positive(self, data: List[Dict], column: str) -> Tuple[bool, List[Dict]]:
        """Check that column values are positive"""
        invalid_records = []
        
        for idx, record in enumerate(data):
            if column in record and record[column] is not None:
                if record[column] <= 0:
                    self.violations.append({
                        'rule': 'POSITIVE',
                        'column': column,
                        'record_id': idx,
                        'message': f"Column '{column}' value {record[column]} is not positive"
                    })
                    invalid_records.append(record)
                    self.invalid_records += 1
        
        return len(invalid_records) == 0, invalid_records
    
    def validate_future_date(self, data: List[Dict], column: str) -> Tuple[bool, List[Dict]]:
        """Check that dates are not in the future"""
        invalid_records = []
        today = datetime.now().date()
        
        for idx, record in enumerate(data):
            if column in record and record[column] is not None:
                if isinstance(record[column], str):
                    try:
                        record_date = datetime.strptime(record[column], '%Y-%m-%d').date()
                    except:
                        continue
                else:
                    record_date = record[column]
                
                if record_date > today:
                    self.violations.append({
                        'rule': 'FUTURE_DATE',
                        'column': column,
                        'record_id': idx,
                        'message': f"Date {record[column]} is in the future"
                    })
                    invalid_records.append(record)
                    self.invalid_records += 1
        
        return len(invalid_records) == 0, invalid_records
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get validation statistics"""
        return {
            'total_records': self.total_records,
            'valid_records': self.valid_records,
            'invalid_records': self.invalid_records,
            'violations': self.violations,
            'validity_rate': (self.valid_records / self.total_records * 100) if self.total_records > 0 else 0
        }
    
    def reset(self):
        """Reset validator state"""
        self.violations = []
        self.total_records = 0
        self.valid_records = 0
        self.invalid_records = 0