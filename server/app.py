from flask import Flask, jsonify, request, make_response
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Pizza , Restaurant_Pizza , Restaurant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restauran.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

ma = Marshmallow(app)

class PizzaSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Pizza
        load_instance = True

    title = ma.auto_field()
    published_at = ma.auto_field()


    url = ma.Hyperlinks(
        {
            "self": ma.URLFor(
                "pizzabyid",
                values=dict(id="<id>")),
            "collection": ma.URLFor("pizzas"),
        }
    )

newsletter_schema = PizzaSchema()
newsletters_schema = PizzaSchema(many=True)

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

        return response

api.add_resource(Index, '/')