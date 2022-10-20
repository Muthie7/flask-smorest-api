from flask import Flask
from flask_smorest import Api

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True ## propagate any flask apps to the view
app.config_["API_TITLE"] = "Stores Rest API"
app.config_["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"]= "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"]= "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)  #connect flask smorest to the flask app

api.register_blueprint(ItemBlueprint)  #register blueprint 
api.register_blueprint(StoreBlueprint)