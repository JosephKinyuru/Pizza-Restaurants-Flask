from flask import Flask, jsonify, request, make_response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, Pizza , RestaurantPizza , Restaurant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

ma = Marshmallow(app)

class RestaurantSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Restaurant
        load_instance = True

restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)

class PizzaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pizza

pizza_schema = PizzaSchema()
pizzas_schema = PizzaSchema(many=True)

class RestaurantPizzaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RestaurantPizza

restaurant_pizza_schema = RestaurantPizzaSchema()

api = Api(app)

class Index(Resource):

    def get(self):

        response_dict = {
            "index": "Welcome to the Pizza-Restaurants RESTful API",
        }

        response = make_response(
            jsonify(response_dict),
            200,
        )
        response.headers["Content-Type"] = "application/json"

        return response

api.add_resource(Index, '/')

class Restaurants(Resource):

    def get(self):

        restaurants = Restaurant.query.all()

        if restaurants :
            response = make_response(
                restaurants_schema.dump(restaurants),
                200,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        else :
            response = make_response(
                jsonify({"error":" Restaurants are not currently in database"}),
                  404
                )
            response.headers["Content-Type"] = "application/json"

            return response

    def post(self):

        new_restaurant = Restaurant(
            name=request.json['name'],
            address=request.json['address'],
        )

        db.session.add(new_restaurant)
        db.session.commit()

        response = make_response(
            restaurant_schema.dump(new_restaurant),
            201,
        )
        response.headers["Content-Type"] = "application/json"

        return response

api.add_resource(Restaurants, '/restaurants')

class RestaurantByID(Resource):

    def get(self, id):

        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant :
            restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id=id).all()
            pizza_data = []

            for rp in restaurant_pizzas:
                pizza = Pizza.query.get(rp.pizza_id)
                if pizza:
                    pizza_data.append({
                        "id": pizza.id,
                        "name": pizza.name,
                        "ingredients": pizza.ingredients
                    })

            response_data = {
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas": pizza_data
            }

            response = make_response(
                jsonify(response_data),
                200,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        else :
            response = make_response(
                jsonify({"error":" Restaurant not found"}),
                  404
                )
            response.headers["Content-Type"] = "application/json"

            return response

    def patch(self, id):

        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant :
            for attr in request.form:
                setattr(restaurant, attr, request.json[attr])

            db.session.add(restaurant)
            db.session.commit()

            response = make_response(
                restaurant_schema.dump(restaurant),
                200
            )
            response.headers["Content-Type"] = "application/json"

            return response

        
        else :
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404
            )
            response.headers["Content-Type"] = "application/json"

            return response

    def delete(self, id):

        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant :
            db.session.delete(restaurant)
            db.session.commit()

            response_dict = {"message": "restaurant successfully deleted"}

            response = make_response(
                jsonify(response_dict),
                200
            )
            response.headers["Content-Type"] = "application/json"

            return response
        else :
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404
                )
            response.headers["Content-Type"] = "application/json"

            return response

api.add_resource(RestaurantByID, '/restaurants/<int:id>')

class Pizzas(Resource):

    def get(self):

        pizzas = Pizza.query.all()

        if pizzas :
            response = make_response(
                pizzas_schema.dump(pizzas),
                200,
            )
            response.headers["Content-Type"] = "application/json"
            
            return response
        
        else :
            response = make_response(
                jsonify({"error":" Pizzas are not currently in database"}),
                  404
                )
            response.headers["Content-Type"] = "application/json"
            return response

    def post(self):

        new_pizza = Pizza(
            name=request.json['name'],
            ingredients=request.json['ingedients'],
        )

        db.session.add(new_pizza)
        db.session.commit()

        response = make_response(
            pizza_schema.dump(new_pizza),
            201,
        )
        response.headers["Content-Type"] = "application/json"

        return response

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):

    def post(self):

        restaurant = Restaurant.query.filter_by(id=request.json['restaurant_id']).first()
        pizza = Pizza.query.filter_by(id=request.json['pizza_id']).first()

        if restaurant and pizza :

            new_restaurant_pizza = RestaurantPizza(
                price=request.json['price'],
                pizza_id=request.json['pizza_id'],
                restaurant_id=request.json['restaurant_id'],
            )

            db.session.add(new_restaurant_pizza)
            db.session.commit()

            response = make_response(
                restaurant_pizza_schema.dump(new_restaurant_pizza),
                201,
            )
            response.headers["Content-Type"] = "application/json"

            return response
        
        else :
            response = make_response(
                  jsonify({"errors": ["validation errors"]}),
                  400
            )
            response.headers["Content-Type"] = "application/json"

            return response
    
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')


@app.errorhandler(NotFound)
def handle_not_found(e):

    response = make_response(
        jsonify({"Not Found": "The requested resource does not exist."}),
        404
    )
    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=5555)