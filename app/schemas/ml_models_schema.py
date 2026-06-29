from marshmallow import Schema, fields, validate, validates, ValidationError


class MlModelSchema(Schema):
    
    id_ml_model = fields.Int(dump_only=True)
    uploaded_by = fields.Int()
    file_path = fields.Str()
    versi = fields.Str()
    r_squared = fields.Float()
    mae = fields.Float()
    is_current = fields.Bool()
    uploaded_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = ("id_ml_model", "uploaded_by", "file_path", "versi", "r_squared", "mae", "is_current", "uploaded_at")


class MlModelCreateSchema(Schema):
    """Schema untuk validasi input form-data create model"""
    
    versi = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=20),
        error_messages={"required": "Versi model wajib diisi"}
    )
    r_squared = fields.Float(required=True, error_messages={"required": "Nilai R-Squared wajib diisi", "invalid": "R-Squared harus berupa angka"})
    mae = fields.Float(required=True, error_messages={"required": "Nilai MAE wajib diisi", "invalid": "MAE harus berupa angka"})

    file = fields.Raw(required=True, error_messages={"required": "File model wajib diunggah"})

    @validates("file")
    def validate_file(self, file_obj, **kwargs):
        if not file_obj or not getattr(file_obj, "filename", None):
            raise ValidationError("File model tidak valid atau kosong")
            
        if not file_obj.filename.lower().endswith('.joblib'):
            raise ValidationError("Ekstensi file tidak diizinkan. Hanya menerima file .joblib")

ml_model_schema = MlModelSchema()
ml_models_schema = MlModelSchema(many=True)
ml_model_create_schema = MlModelCreateSchema()