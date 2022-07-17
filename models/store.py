from db import db

class StoreModel(db.Model):
    # telling sql alchemy the table names and there columns
    __tablename__ = 'stores'
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel' , lazy = 'dynamic') # gets all the items from the ItemModel corresponding to the store_id

    # this creates an object for every item in a store, which may cause a lot of resources
    # so putting lazy = dynamic will prevent sql alchemy from making an object for every item
    # but as it does not create a list of objects anymore instead it creates a querybuilder object just like .query
    # we need to do .all() to make the querybuilder object into a list of objects

    def __init__(self , name):
        self.name = name

    # returns a json representation of the model
    def json(self):
        return { 'name' : self.name , 'items' : [item.json() for item in self.items.all()] }
    

    # this method is to find an item in the database by name
    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name = name).first()
    
    # this method is to insert an item in the database
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # deleting from db:
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()