from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    item_id = fields.Int(dump_only=True)  #not used for validation when data is coming from rqst
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    store_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    location = fields.Str(required=True)

class PlainTagSchema(Schema):
    tag_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)  #only used when returning data to client
    tags = fields.List(fields.Nested(PlainTagSchema()),dump_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str() #no options,indicate they are optional
    price = fields.Float()
    store_id = fields.Int()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema(),dump_only=True))
    tags = fields.List(fields.Nested(PlainTagSchema(),dump_only=True))


class TagSchema(PlainTagSchema):
    store_id = fields.Int(required=False, load_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(),dump_only=True)  #only used when returning data to client

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)