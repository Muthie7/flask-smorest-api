from email import message
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores",__name__, desciption="Stores Operations")

# connect Flask Smorest with the Store Class methodview
#make a get rqst it goes to below route
@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id], 200
        except KeyError as e:
            abort(404, message="Store not found!!")

    def delete(self,store_id):
        try:
            del stores[store_id]
            return {"message":"store deleted"}
        except KeyError:
            abort(404,message="Store Not Found!")

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}
    
    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(404,message="Bad Request. Ensure 'name' in the JSON payload.")
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(404,message="Store already exists.")
        store_id = uuid.uuid4().hex
        store = {
            **store_data,
            "store_id": store_id
        }
        stores[store_id] = store
        return store, 201

