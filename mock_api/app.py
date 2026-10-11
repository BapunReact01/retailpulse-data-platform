from flask import Flask, jsonify
from flask_cors import CORS
from routes.customers import customers_bp
from routes.products import products_bp
from routes.stores import stores_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(customers_bp, url_prefix='/api/v1')
app.register_blueprint(products_bp, url_prefix='/api/v1')
app.register_blueprint(stores_bp, url_prefix='/api/v1')

@app.route('/')
def index():
    return jsonify({
        'message': 'RetailPulse Mock API',
        'version': '1.0.0',
        'endpoints': {
            'customers': '/api/v1/customers',
            'products': '/api/v1/products',
            'stores': '/api/v1/stores'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)