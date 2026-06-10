from marshmallow import Schema, fields, validate


class PredictSchema(Schema):
    """Schema untuk validasi input prediksi harga mobil"""

    id_model = fields.Int(required=True, error_messages={"required": "ID Model Kendaraan wajib diisi."})
    tahun = fields.Int(
        required=True,
        validate=validate.Range(min=1980, max=2027),
        error_messages={"required": "Tahun mobil wajib diisi."}
    )
    mileage = fields.Int(
        required=True,
        validate=validate.Range(min=0),
        error_messages={"required": "Mileage wajib diisi."}
    )
    transmisi = fields.Str(required=True, error_messages={"required": "Transmisi wajib diisi."})
    bahan_bakar = fields.Str(required=True, error_messages={"required": "Bahan bakar wajib diisi."})
    pajak = fields.Int(required=True, validate=validate.Range(min=0), error_messages={"required": "Pajak wajib diisi."})
    mpg = fields.Float(required=True, validate=validate.Range(min=0), error_messages={"required": "MPG wajib diisi."})
    kapasitas_mesin = fields.Float(required=True, validate=validate.Range(min=0), error_messages={"required": "Kapasitas mesin wajib diisi."})

class SavePredictionSchema(PredictSchema):
    """Schema untuk validasi input saat menyimpan riwayat prediksi"""
    
    id_ml_model = fields.Int(required=True, error_messages={"required": "ID Model ML wajib diisi."})
    harga_prediksi = fields.Float(required=True, error_messages={"required": "Harga prediksi wajib diisi."})
    shap_summary = fields.Raw(required=True, error_messages={"required": "Nilai SHAP summary wajib diisi."})

predict_schema = PredictSchema()
save_prediction_schema = SavePredictionSchema()