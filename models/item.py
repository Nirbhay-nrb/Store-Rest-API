from db import db

class ItemModel(db.Model):
    # telling sql alchemy the table names and there columns
    __tablename__ = 'items'
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2)) # precision is the number of digits after decimal

    store_id = db.Column(db.Integer , db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') # this sees the store_id and automatically gets the store from the StoreModel

    def __init__(self , name , price , store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # returns a json representation of the model
    def json(self):
        return { 'name' : self.name , 'price' : self.price }
    

    # this method is to find an item in the database by name
    @classmethod
    def find_by_name(cls,name):
        # .query comes from sqlalchemy
        return ItemModel.query.filter_by(name = name).first() # you can just use cls instead of ItemModel as this is a class method
        # returns the first row of the output of the query
        # return type = ItemModel object
    
    # this method is to insert an item in the database
    def save_to_db(self):
        db.session.add(self) # if the object contains an id, then the item is updated otherwise a new item is inserted
        # self is the ItemModel object, and sqlalchemy automatically translate the object into a row
        db.session.commit()

    # deleting from db:
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()