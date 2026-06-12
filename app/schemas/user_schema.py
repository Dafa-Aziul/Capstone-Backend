from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id_user = fields.Int()
    nama = fields.Str()
    email = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()
    
class UserUpdateSchema(Schema):
    status = fields.Bool(required=True,error_messages={"required": "Status wajib diisi"})
    

users_schema = UserSchema(many=True)
update_status = UserUpdateSchema()
