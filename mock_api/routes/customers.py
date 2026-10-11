from flask import Blueprint, jsonify, request
from models.customer_data import CUSTOMERS

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    return jsonify({
        'data': CUSTOMERS,
        'count': len(CUSTOMERS)
    })

@customers_bp.route('/customers/<customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a specific customer by ID"""
    customer = next((c for c in CUSTOMERS if c['customer_id'] == customer_id), None)
    if customer:
        return jsonify(customer)
    return jsonify({'error': 'Customer not found'}), 404
