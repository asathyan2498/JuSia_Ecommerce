from flask import Flask, request, jsonify
from models import db, Product
from db_setup import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
init_db(app)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], stock=data['stock'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created", "product": new_product.to_dict()}), 201

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify(product.to_dict()), 200

@app.route('/products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    data = request.json
    product.name = data['name']
    product.price = data['price']
    product.stock = data['stock']
    db.session.commit()
    return jsonify({"message": "Product updated", "product": product.to_dict()}), 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
