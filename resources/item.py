from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

# resources
class Item(Resource):
    parser = reqparse.RequestParser() # initialising a new object 
    # adding an argument(price) to the parser 
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank!'
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = 'Every item needs a store id'
    )

    # retrieves an item from the list that matches the name given
    @jwt_required() 
    def get(self,name):
        item = ItemModel.find_by_name(name) # item object
        if item:
            return item.json() # .json() is our own function
        return {'message' : 'Item not found'},404


    # creating an item
    def post(self,name):
        if ItemModel.find_by_name(name):
            # that means there is already an item with the given name 
            return {'message' : f'An item with name \'{name}\' already exists'}, 400
            # 400 represents bad request

        # item does not exist
        data = Item.parser.parse_args() 
        item = ItemModel(name , data['price'] , data['store_id'])
        # inserting the item in database
        try: 
            item.save_to_db()
        except: # database error
            return {'message' : 'An error occured in inserting the item'} , 500 # internal server error
        return item.json(),201 
        # 201 represents created

    # deleting an item
    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message' : 'Item deleted'}

    # updating the items (creating if item doesnt exist)
    def put(self,name):
        data = Item.parser.parse_args() 
        item = ItemModel.find_by_name(name)
        # it item exists then item will be returned otherwise it would be None
        if item is None: # create the item
            item = ItemModel(name , data['price'] , data['store_id']) # no id that means this item will be inserted
        else: # update the item
            item.price = data['price'] # there is already an id in this and we update the price
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    # getting the list of items
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}