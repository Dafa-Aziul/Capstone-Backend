from marshmallow import Schema, fields, validate


class MerekSchema(Schema):
    id_merek = fields.Int(dump_only=True)
    nama_merek = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    class Meta:
        # Field yang di-include dalam response
        fields = ('id_merek', 'nama_merek')


class MerekCreateSchema(Schema):
    nama_merek = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=30),
        error_messages={'required': 'Nama merek wajib diisi'}
    )


# Instance untuk reuse
merek_schema = MerekSchema()
mereks_schema = MerekSchema(many=True)
merek_create_schema = MerekCreateSchema()
