from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self , name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message' : 'No such store exists'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            # store exists
            return {'message' : f'A story already exists with the name \'{name}\''} , 400
        
        # store doesnt exist
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message' : 'An error occured while creating the store'} , 500 # internal server error
        return store.json() , 201 # for created


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message' : 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores' : [store.json() for store in StoreModel.query.all()]}