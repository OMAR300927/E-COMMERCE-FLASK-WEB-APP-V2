from ..extension import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_password = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='user')
    auth_provider = db.Column(db.String(20), nullable=False, default='local')

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)
    

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255))

    def __repr__(self):
        return f'<Products {self.name}>'
    

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'amount': self.amount,
            'image': self.image
        }
    

class ShoppingCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Products')
    
    def __repr__(self):
        return f'<ShoppingCart User: {self.user_id}, Product: {self.product_id}, Quantity: {self.quantity}>'
    

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Payment User: {self.user_id}, Amount: {self.amount}, Status: {self.status}>'
    