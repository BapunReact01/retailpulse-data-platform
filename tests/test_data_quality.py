import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_quality.validators import DataValidator
from data_quality.quarantine import QuarantineHandler
from data_quality.quality_report import QualityReport


def test_validate_not_null():
    """Test NOT NULL validation"""
    validator = DataValidator()
    
    data = [
        {'id': 1, 'name': 'Test'},
        {'id': 2, 'name': None},  # Invalid
        {'id': 3, 'name': 'Test2'},
    ]
    
    is_valid, invalid = validator.validate_not_null(data, ['id', 'name'])
    
    assert not is_valid
    assert len(invalid) == 1
    assert invalid[0]['id'] == 2


def test_validate_positive():
    """Test positive value validation"""
    validator = DataValidator()
    
    data = [
        {'id': 1, 'price': 100},
        {'id': 2, 'price': -50},  # Invalid
        {'id': 3, 'price': 200},
    ]
    
    is_valid, invalid = validator.validate_positive(data, 'price')
    
    assert not is_valid
    assert len(invalid) == 1
    assert invalid[0]['id'] == 2


def test_validate_range():
    """Test range validation"""
    validator = DataValidator()
    
    data = [
        {'id': 1, 'score': 85},
        {'id': 2, 'score': 150},  # Invalid (outside 0-100)
        {'id': 3, 'score': 90},
    ]
    
    is_valid, invalid = validator.validate_range(data, 'score', 0, 100)
    
    assert not is_valid
    assert len(invalid) == 1
    assert invalid[0]['id'] == 2


def test_validate_email_format():
    """Test email format validation"""
    validator = DataValidator()
    
    data = [
        {'id': 1, 'email': 'test@example.com'},
        {'id': 2, 'email': 'invalid-email'},  # Invalid
        {'id': 3, 'email': 'valid@test.com'},
    ]
    
    is_valid, invalid = validator.validate_email_format(data, 'email')
    
    assert not is_valid
    assert len(invalid) == 1
    assert invalid[0]['id'] == 2


def test_quarantine_handler():
    """Test quarantine handler"""
    quarantine = QuarantineHandler("data/quarantine")
    
    invalid_records = [
        {'id': 1, 'reason': 'NULL_VIOLATION'},
        {'id': 2, 'reason': 'FORMAT_VIOLATION'},
    ]
    
    filepath = quarantine.quarantine_records(invalid_records, 'test_source', 'Test reason')
    
    assert filepath is not None
    assert 'test_source' in filepath
    assert os.path.exists(filepath)


def test_quality_report():
    """Test quality report generation"""
    report = QualityReport("data/quality_reports")
    
    statistics = {
        'total_records': 100,
        'valid_records': 95,
        'invalid_records': 5,
        'violations': []
    }
    
    filepath = report.generate_report('test_layer', statistics, [])
    
    assert filepath is not None
    assert 'test_layer' in filepath
    assert os.path.exists(filepath)