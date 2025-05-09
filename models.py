from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import LargeBinary
from flask_login import UserMixin

db = SQLAlchemy()

class RoleEnum(Enum):
    ADMIN = 'admin'
    USER = 'user'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    role = db.Column(SqlEnum(RoleEnum, name="role_enum"), default=RoleEnum.USER, nullable=False)

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.String(10), nullable=False)
    image = db.Column(LargeBinary, nullable=False)
    image_mime = db.Column(db.String(50), nullable=False)
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('dish.id'), nullable=False)
    product = db.relationship('Dish', backref=db.backref('orders', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer = db.relationship('User', backref=db.backref('orders', lazy=True))
    delivery_address = db.Column(db.String(200), nullable=False)
    comment = db.Column(db.String(200))
    
    



