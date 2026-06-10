from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    """Schema untuk request login"""
    email = fields.Email(
        required=True,
        error_messages={"required": "Email wajib diisi", "invalid": "Format email tidak valid"}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={"required": "Password wajib diisi"}
    )


class RegisterSchema(Schema):
    """Schema untuk request register"""
    nama = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Nama wajib diisi"}
    )
    email = fields.Email(
        required=True,
        error_messages={"required": "Email wajib diisi", "invalid": "Format email tidak valid"}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={"required": "Password wajib diisi"}
    )

login_schema = LoginSchema()
register_schema = RegisterSchema()