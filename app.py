import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db

# import models  #imported before loading sqlalchemy

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

def create_app(db_url=None):
    app= Flask(__name__, instance_path=os.getcwd())

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    #DB
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    api = Api(app)  #connect flask smorest to the flask app

    app.config["JWT_SECRET_KEY"] ="spartan"
    jwt = JWTManager(app)

    with app.app_context():
        import models

        db.create_all()  #runs before any api rqst/if table exists its skipped

    api.register_blueprint(ItemBlueprint)  #register blueprint 
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    return app

if __name__ == '__main__':
    create_app()