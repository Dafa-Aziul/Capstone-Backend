from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id_user = fields.Int()
    nama = fields.Str()
    email = fields.Str()
    is_active = fields.Bool()
    created_at = fields.DateTime()
    
class UserUpdateSchema(Schema):
    status = fields.Bool(required=True,error_messages={"required": "Status wajib diisi"})


class CreateAdminSchema(Schema):
    nama = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Nama wajib diisi"},
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "Email wajib diisi",
            "invalid": "Format email tidak valid",
        },
    )


users_schema = UserSchema(many=True)
update_status = UserUpdateSchema()
create_admin_schema = CreateAdminSchema()
