from db import db

class ItemModel(db.Model):  #mapping btwn a row in a table and a python class
    #create the table
    __tablename__ = "items"
    #create the columns
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.store_id"),unique=False,nullable=False)

    store = db.relationship("StoreModel",back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
