#!/usr/bin/env python3

from faker import Faker

from app import app
from models import db, Pizza, Restaurant, RestaurantPizza

with app.app_context():
    fake = Faker()

    try:
        Pizza.query.delete()
    except Exception as e:
        pass

    pizzas = []
    for i in range(25):
        pizza = Pizza(
            name=fake.unique.first_name(),
            ingredients=fake.paragraph(nb_sentences=5),
        )
        pizzas.append(pizza)

    db.session.add_all(pizzas)
    db.session.commit()

    try:
        Restaurant.query.delete()
    except Exception as e:
        pass

    restaurants = []
    for i in range(25):
        restaurant = Restaurant(
            name=fake.unique.company(),
            address=fake.address(),
        )
        restaurants.append(restaurant)

    db.session.add_all(restaurants)
    db.session.commit()

    try:
        RestaurantPizza.query.delete()
    except Exception as e:
        pass

    for i in range(25):
        restaurant_pizza = RestaurantPizza(
            price=fake.random_int(min=1, max=30),
            pizza_id=fake.random_element(elements=pizzas).id,
            restaurant_id=fake.random_element(elements=restaurants).id
        )
        db.session.add(restaurant_pizza)

    db.session.commit()
