import json
from marshmallow import Schema, fields, validate
from app.schemas.ml_models_schema import MlModelSchema


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
            else "Unknown Model"
        )
    )
    created_at = fields.DateTime()


class RiwayatPrediksiByUser(Schema):
    id_riwayat = fields.Int()
    mobil = fields.Function(
        lambda obj: (
            f"{obj.model_kendaraan.merek.nama_merek} {obj.model_kendaraan.nama_model}".strip()
            if obj.model_kendaraan and obj.model_kendaraan.merek
            else ""
        )
    )
    harga_prediksi = fields.Float()
    created_at = fields.DateTime()

class RiwayatPrediksiDetail(Schema):
    id_riwayat = fields.Int()
    created_at = fields.DateTime()
    
    # 1. Rename harga_prediksi menjadi prediction menggunakan parameter attribute
    prediction = fields.Float(attribute="harga_prediksi")
    
    # 2. Rename ml_model menjadi model_info dan tambah id_ml_model
    model_info = fields.Nested(
        MlModelSchema, 
        only=("id_ml_model", "versi", "r_squared", "mae"), 
        attribute="ml_model"
    )
    # 3. Kelompokkan properti mobil ke dalam object input_data
    input_data = fields.Method("get_input_data")
    
    
    # 4. Rename shap_summary menjadi shap_explanation
    shap_explanation = fields.Method("get_shap_summary")
    

    def get_input_data(self, obj):
        if not obj:
            return {}
        return {
            "merk": obj.model_kendaraan.merek.nama_merek if getattr(obj, "model_kendaraan", None) and getattr(obj.model_kendaraan, "merek", None) else "",
            "model": obj.model_kendaraan.nama_model if getattr(obj, "model_kendaraan", None) else "",
            "year": obj.tahun,
            "mileage": obj.mileage,
            "transmission": obj.transmisi,
            "fuelType": obj.bahan_bakar,
            "tax": obj.pajak,
            "mpg": obj.mpg,
            "engineSize": obj.kapasitas_mesin
        }

    def get_shap_summary(self, obj):
        if obj and getattr(obj, "shap_summary", None):
            try:
                # Parsing string JSON dari database menjadi Object/Dictionary
                return json.loads(obj.shap_summary)
            except (ValueError, TypeError):
                return obj.shap_summary
        return None

predict_schema = PredictSchema()
save_prediction_schema = SavePredictionSchema()
predicts_schema = RiwayatPrediksiSchema(many=True)
predict_by_user_schema = RiwayatPrediksiByUser(many=True)
predict_detail_schema = RiwayatPrediksiDetail()
