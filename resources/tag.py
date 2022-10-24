from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("Tags",__name__, description="Operations on tags")

@blp.route("/store/<string:store_id>/tag")  # Retrival of tags in a store
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))  
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201,TagSchema)
    def post(self,tag_data,store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))
        
        return tag

# Linking/Unlinkins tags from items
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):  # doesnt create a new tag simply just links the tag found to an item found
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return tag

    @blp.response(200,TagAndItemSchema)
    def delete(self,item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try: 
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return {
            "message":"Tag removed from Item", 
            "item":item, 
            "tag":tag
            }

@blp.route("/tags/<int:tag_id>") #retrive info on specific tag
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202, 
        description="Deletes a tag if no item is tagged with it.",
        example={"message":"Tag deleted."})
    @blp.alt_response(404,description="Tag Not Found!")
    @blp.alt_response(400,description="Returned if tag still attached to an item, cant be deleted!")
    def delete(self,tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"Tag deleted."}
        abort(
            400,
            message ="Could not delete tag.Ensure tag not associated with any items."
        )
        
