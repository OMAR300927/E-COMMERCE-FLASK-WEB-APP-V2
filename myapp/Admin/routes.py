from flask import Blueprint, jsonify, request
from ..modules.model import Products, Users
from ..decorators.role import role_required
from ..modules.services import save, delete


admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# Get all products
@admin_bp.route('/all-products', methods=['GET'])
@role_required('admin')
def all_products():
    data = Products.query.all()
    return jsonify([product.to_dict() for product in data])

# Add product
@admin_bp.route('/add-product', methods=['POST'])
@role_required('admin')
def add_product():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    name = data.get('name')
    price = data.get('price')
    amount = data.get('amount')
    image = data.get('image')

    if not name or price is None or amount is None or not image:
        return jsonify({'message': 'You must provide all product data'}), 400
    
    new_product = Products(name=name, price=price, amount=amount, image=image)
    save(new_product)
    return jsonify({'message': 'Product added successfully'}), 201

# Update product
@admin_bp.route('/update-product/<int:product_id>', methods=['PATCH'])
@role_required('admin')
def update_product(product_id):
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    product = Products.query.get(product_id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    name = data.get('name')
    price = data.get('price')
    amount = data.get('amount')
    image = data.get('image')

    if name:
        product.name = name

    if price is not None:
        product.price = price
        
    if amount is not None:
        product.amount = amount

    if image:
        product.image = image


    save(product)
    return jsonify({'message': 'Product updated successfully'}), 200

# Delete product
@admin_bp.route('/delete-product/<int:product_id>', methods=['DELETE'])
@role_required('admin')
def delete_product(product_id):
    product = Products.query.get(product_id)

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    delete(product)
    return jsonify({'message': 'Product deleted successfully'}), 200

# See all users
@admin_bp.route('/all-users', methods=['GET'])
@role_required('admin')
def all_users():
    data = Users.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role} for user in data])