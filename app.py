import functools
import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items, users

#Handle some errors here
class PermissionError(RuntimeError):
    pass

app = Flask(__name__)

## UserCheck middleware
def make_secure(name):
    def outer(func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            for user in users:
                if user["username"] == name:
                    if user["password"] == "pass1234":
                        return func(*args,**kwargs)
                raise PermissionError("You are not authorized!")
        return inner
    return outer

# GET Home
@app.get('/')
@make_secure("spartan")
def home():
    return """
        <h2>Welcome to the "smorest" store api</h2>
    """


#### STORES
# GET All Stores
@app.get('/store') # http://localhost:5000/store
def get_stores():
    return {"stores": list(stores.values())}

#Get A Store
@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id], 200
    except KeyError as e:
        abort(404, message="Store not found!!")


# POST New Store
@app.post('/store')
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:  ## Validation, replaced with MASHMELLOW!!
        abort(
            400,
            message="Bad request. Ensure 'name' is included in JSON payload."
        )
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(
                400,
                message="Store already existing!"
            )

    store_id = uuid.uuid4().hex
    store = {
        **store_data,
        "store_id": store_id
    }
    stores[store_id] = store
    return store, 201

# DELETE STORE
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"Store deleted!"}
    except KeyError:
        abort(
            404,
            message="Store Not Found!"
        )


#### ITEMS
#Get all items
@app.get("/item")
def get_all_items():
    return {
        "items": list(items.values())
    }, 200

#Get Single Item
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id], 200
    except KeyError: 
        abort(404, message="Item not found!")

# POST new item 
@app.post('/item')
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad Request. Ensure 'price','store_id','name' included in the JSON payload."
        )

    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item already exist.")
    
    if item_data["store_id"] not in stores:
        abort(404, message="Store not found!")
        
    item_id = uuid.uuid4().hex
    item = {
        ** item_data,
        "item_id": item_id
    }
    items[item_id] = item
    return item, 201

#Update Item, Price
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if(
        "price" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad Request. Ensure 'price' and 'name' included in JSON payload!"
        )
    try:
        item = items[item_id]
        item |= item_data ## in-place modification,,any values of item_data replace first,item
        return item, 201
    except KeyError:
        abort(404,message="Item not found")


# Delete Item
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item deleted!"}, 204
    except KeyError:
        abort(
            404,
            message="Item not found!"
            )
