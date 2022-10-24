from enum import unique
from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    store_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True,nullable=False)
    location = db.Column(db.String(80),unique=False,nullable=False)
    tags = db.relationship("TagModel",back_populates="store",lazy="dynamic")
    items = db.relationship("ItemModel",back_populates="store", lazy="dynamic")