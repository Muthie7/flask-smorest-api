from email import message
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from db import db
from models import UserModel
from schemas import UserSchema
from sqlalchemy.exc import SQLAlchemyError,IntegrityError

blp = Blueprint("users", __name__, description="Operations on Users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()

        except IntegrityError:
            abort(409, message="User with username already exists.")
        except SQLAlchemyError:
            abort(
                500,
                message="Error Inserting User to Db."
            )
        
        return user

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password): #compare/verify input passwd from pass in db
            access_token = create_access_token(identity=user.user_id) #pass user_id to be stored in the access token
            return {
                "access_token": access_token
            }
        abort(401, message="Invalid credentials!!")

#(DEV)
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200,UserSchema)
    def get(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        print(user)
        return user

    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message":"User deleted successfully"}, 200

