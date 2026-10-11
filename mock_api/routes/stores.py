from flask import Blueprint, jsonify, request
from models.store_data import STORES

stores_bp = Blueprint('stores', __name__)

@stores_bp.route('/stores', methods=['GET'])
def get_stores():
    """Get all stores"""
    return jsonify({
        'data': STORES,
        'count': len(STORES)
    })

@stores_bp.route('/stores/<store_id>', methods=['GET'])
def get_store(store_id):
    """Get a specific store by ID"""
    store = next((s for s in STORES if s['store_id'] == store_id), None)
    if store:
        return jsonify(store)
    return jsonify({'error': 'Store not found'}), 404