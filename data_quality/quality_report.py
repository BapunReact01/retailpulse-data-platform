import json
import os
from typing import Dict, Any, List
from datetime import datetime


class QualityReport:
    """Generate data quality reports"""
    
    def __init__(self, report_dir: str = "data/quality_reports"):
        self.report_dir = report_dir
        os.makedirs(report_dir, exist_ok=True)
    
    def generate_report(self, layer: str, statistics: Dict[str, Any], violations: List[Dict]) -> str:
        """Generate quality report for a data layer"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{layer}_quality_report_{timestamp}.json"
        filepath = os.path.join(self.report_dir, filename)
        
        report = {
            'layer': layer,
            'timestamp': datetime.now().isoformat(),
            'statistics': statistics,
            'violations': violations,
            'status': 'PASS' if statistics['validity_rate'] >= 95 else 'FAIL'
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Quality report generated: {filepath}")
        return filepath
    
    def generate_summary(self, layer_reports: List[str]) -> Dict[str, Any]:
        """Generate summary across all layers"""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'layers': [],
            'overall_status': 'PASS',
            'total_violations': 0
        }
        
        for report_file in layer_reports:
            with open(report_file, 'r') as f:
                report = json.load(f)
                summary['layers'].append({
                    'layer': report['layer'],
                    'status': report['status'],
                    'validity_rate': report['statistics']['validity_rate'],
                    'violation_count': len(report['violations'])
                })
                summary['total_violations'] += len(report['violations'])
                
                if report['status'] == 'FAIL':
                    summary['overall_status'] = 'FAIL'
        
        summary['total_layers'] = len(layer_reports)
        summary['passed_layers'] = sum(1 for l in summary['layers'] if l['status'] == 'PASS')
        summary['failed_layers'] = summary['total_layers'] - summary['passed_layers']
        
        return summary