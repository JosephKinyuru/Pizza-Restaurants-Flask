from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from wtforms.validators import Length, ValidationError, DataRequired

db = SQLAlchemy()

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    restaurant_pizza = db.relationship('RestaurantPizza', back_populates='pizza')

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String)
    
    restaurant_pizza = db.relationship('RestaurantPizza', back_populates='restaurant')

    @validates('name')
    def validate_name(self, key, name):
        if len(name) >= 50:
            raise ValueError("Name must be less than 50 characters")
        return name

class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    pizza = db.relationship('Pizza', back_populates='restaurant_pizza')
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizza')

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30")
        return price
