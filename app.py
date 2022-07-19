import os

from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item , ItemList
from resources.store import StoreList , Store
from db import db

# creating app and api
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL' , 'sqlite:///data.db')
# if the get method return None (that is the app is not running on heroku's computer), then the data.db on our computer will be used
# telling the app from where to find the data.db file 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off the Flask_sqlalchemy tracker for changes as it cost some resources
# however this does not turn off the underlying sqlalchemy tracker
app.secret_key = 'jose'
api = Api(app)

# setting up JWT with the secret key
app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app,authenticate , identity) # authenticate and identity imported from security
# config JWT to expire within hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)

# adding the resource
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# running the app
if __name__ == '__main__': # if in case app.py is imported then this if block won't be run
    db.init_app(app)
    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()
    app.run(port=5000) 
# as when we import a file, python actually runs the file and we dont want the app to be running again 