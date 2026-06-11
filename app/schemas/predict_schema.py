from marshmallow import Schema, fields, validate


class PredictSchema(Schema):
    id_model = fields.Int(
        required=True, error_messages={"required": "ID Model Kendaraan wajib diisi."}
    )
    tahun = fields.Int(
        required=True,
        validate=validate.Range(min=1980, max=2027),
        error_messages={"required": "Tahun mobil wajib diisi."},
    )
    mileage = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        error_messages={"required": "Mileage wajib diisi."},
    )
    transmisi = fields.Str(
        required=True, error_messages={"required": "Transmisi wajib diisi."}
    )
    bahan_bakar = fields.Str(
        required=True, error_messages={"required": "Bahan bakar wajib diisi."}
    )
    pajak = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        error_messages={"required": "Pajak wajib diisi."},
    )
    mpg = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        error_messages={"required": "MPG wajib diisi."},
    )
    kapasitas_mesin = fields.Float(
        required=True,
        validate=validate.Range(min=0),
        error_messages={"required": "Kapasitas mesin wajib diisi."},
    )


class SavePredictionSchema(PredictSchema):
    id_ml_model = fields.Int(
        required=True, error_messages={"required": "ID Model ML wajib diisi."}
    )
    harga_prediksi = fields.Float(
        required=True, error_messages={"required": "Harga prediksi wajib diisi."}
    )
    shap_summary = fields.Raw(
        required=True, error_messages={"required": "Nilai SHAP summary wajib diisi."}
    )


class RiwayatPrediksiSchema(Schema):
    # Gunakan fields.Function untuk mapping kustom mirip seperti cara Anda sebelumnya
    nama_user = fields.Function(
        lambda obj: (
            obj.user.nama if obj.user and hasattr(obj.user, "nama") else "Unknown User"
        )
    )
    email = fields.Function(lambda obj: obj.user.email if obj.user else "Unknown Email")
    mobil = fields.Function(
        lambda obj: (
            f"{obj.model_kendaraan.merek.nama_merek} {obj.model_kendaraan.nama_model}".strip()
            if obj.model_kendaraan and obj.model_kendaraan.merek
            else ""
        )
    )
    harga_prediksi = fields.Float()
    ml_model = fields.Function(
        lambda obj: (
            obj.ml_model.versi
            if obj.ml_model and hasattr(obj.ml_model, "versi")
            else "Unknown Mode"
        )
    )
    created_at = fields.DateTime()


class RiwayatPrediksiByUser(Schema):
    mobil = fields.Function(
        lambda obj: (
            f"{obj.model_kendaraan.merek.nama_merek} {obj.model_kendaraan.nama_model}".strip()
            if obj.model_kendaraan and obj.model_kendaraan.merek
            else ""
        )
    )
    harga_prediksi = fields.Float()
    created_at = fields.DateTime()
    ml_model = fields.Function(
        lambda obj: (
            obj.ml_model.versi
            if obj.ml_model and hasattr(obj.ml_model, "versi")
            else "Unknown Mode"
        )
    )

predict_schema = PredictSchema()
save_prediction_schema = SavePredictionSchema()
predicts_schema = RiwayatPrediksiSchema(many=True)
predict_by_user_schema = RiwayatPrediksiByUser(many=True)
