from email import message
from sqlite3 import IntegrityError
import uuid
# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores",__name__)

# connect Flask Smorest with the Store Class methodview

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    @blp.response(204)
    def delete(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store deleted."}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400,message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500,message="An error occured inserting store.")
        return store

