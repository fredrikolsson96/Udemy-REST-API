import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

# create application, secret key, and API
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'key'
api = Api(app)

# create JWT object
# this creates a new endpoint: /auth
jwt = JWT(app, authenticate, identity)

# add the store, store-list, item, item-list and user-register resources to the API
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# prevent application from starting when importing app module
if __name__ == '__main__':
    db.init_app(app) 

    # start the application
    app.run(port=5000, debug=True)