from flask import Blueprint, jsonify, request
from models.product_data import PRODUCTS

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    """Get all products"""
    return jsonify({
        'data': PRODUCTS,
        'count': len(PRODUCTS)
    })

@products_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    product = next((p for p in PRODUCTS if p['product_id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404