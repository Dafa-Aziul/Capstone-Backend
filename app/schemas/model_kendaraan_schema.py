from marshmallow import Schema, fields, validate


class ModelKendaraan(Schema):
    id_model = fields.Int(dump_only=True)
    id_merek = fields.Int(dump_only=True)
    nama_merek = fields.Function(
        lambda obj: (
            obj.merek.nama_merek
            if obj.merek and hasattr(obj.merek, "nama_merek")
            else "Unknown Merek"
        )
    )
    nama_model = fields.Str(required=True, validate=validate.Length(min=1, max=50))

    class Meta:
        fields = ("id_model", "id_merek", "nama_merek", "nama_model")


class ModelKendaraanCreate(Schema):
    id_merek = fields.Int(
        required=True, error_messages={"required": "ID merek wajib diisi"}
    )

    nama_model = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50),
        error_messages={"required": "Nama model kendaraan wajib diisi"},
    )


class ModelKendaraanUpdateSchema(Schema):
    id_merek = fields.Int(required=True)
    nama_model = fields.Str(required=True, validate=validate.Length(min=1, max=50))


model_kendaraan_schema = ModelKendaraan()
model_kendaraans_schema = ModelKendaraan(many=True)
model_kendaraan_create = ModelKendaraanCreate()
model_kendaraan_update = ModelKendaraanUpdateSchema()
