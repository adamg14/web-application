from shop import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    shoppingbaskets = db.relationship('ShoppingBasket', backref='customer', lazy='dynamic')

    def __repr__(self):
        return f"User: {self.username}"
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(15), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.png")
    description = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    shoppingbaskets = db.relationship('ShoppingBasket', backref='product', lazy='dynamic')
    # could add calories NEED TO ADD MUCH MORE ITEMS


    def __repr__(self):
        return f"Product: {self.product_name}"


class ShoppingBasket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return f'shopping basket item number: {self.id}'
