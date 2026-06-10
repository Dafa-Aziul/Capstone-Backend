import os
import json
from datetime import datetime
import pandas as pd
import numpy as np

from flask import current_app
from app.repositories.ml_models_repository import MlModelsRepository
from app.repositories.model_kendaraan_repository import ModelKendaraanRepository
from app.repositories.predict_repository import PredictRepository
from app.utils.ml_utils import (
    load_ml_artifacts,
    get_clean_feature_names,
    transform_to_dataframe,
    generate_shap_explanation
)


class PredictService:
    @staticmethod
    def predict(input_data):
        # 1. Dapatkan model ML yang aktif
        active_model = MlModelsRepository.get_active_model()
        if not active_model:
            raise ValueError("Tidak ada model ML yang aktif saat ini.")

        # 2. Load model dan preprocessor dari file .joblib
        project_root = os.path.dirname(current_app.root_path)
        model_path = os.path.join(project_root, active_model.file_path)
        
        if not os.path.exists(model_path):
            raise FileNotFoundError("File model .joblib tidak ditemukan di server.")
            
        model, preprocessor = load_ml_artifacts(model_path)

        # 3. Ambil nama merek dan model dari ID Model
        model_kendaraan = ModelKendaraanRepository.get_by_id(input_data['id_model'])
        
        if not model_kendaraan:
            raise ValueError(f"Model kendaraan dengan ID {input_data['id_model']} tidak ditemukan.")
            
        merek = model_kendaraan.merek
        if not merek:
            raise ValueError("Data Merek untuk model kendaraan ini tidak ditemukan.")

        # 4. Siapkan data input untuk di-encode dan diprediksi
        raw_data_for_prediction = {
            'merk': [merek.nama_merek],
            'model': [model_kendaraan.nama_model],
            'year': [input_data['tahun']],
            'mileage': [input_data['mileage']],
            'transmission': [input_data['transmisi']],
            'fuelType': [input_data['bahan_bakar']],
            'tax': [input_data['pajak']],
            'mpg': [input_data['mpg']],
            'engineSize': [input_data['kapasitas_mesin']]
        }
        input_df = pd.DataFrame(raw_data_for_prediction)

        # 5. Encode data menggunakan preprocessor yang sudah di-load
        try:
            transformed_data = preprocessor.transform(input_df)
            clean_feature_names = get_clean_feature_names(preprocessor)
            transformed_data = transform_to_dataframe(transformed_data, clean_feature_names)
        except Exception as e:
            raise RuntimeError(f"Gagal melakukan transformasi data (encoding): {e}")

        # 6. Lakukan prediksi
        prediction_result = model.predict(transformed_data)
        
        # Pastikan result diambil sebagai skalar dengan aman
        predicted_price = float(np.asarray(prediction_result).flatten()[0])

        # 7. Hitung SHAP values untuk explainability
        shap_json = generate_shap_explanation(model, transformed_data, clean_feature_names)

        # 8. Kembalikan hasil lengkap (tanpa simpan ke database)
        return {
            "input_data": raw_data_for_prediction,
            "prediction": predicted_price,
            "shap_explanation": shap_json,
            "model_info": {
                "id_ml_model": active_model.id_ml_model,
                "versi": active_model.versi,
                "r_squared": float(active_model.r_squared),
                "mae": float(active_model.mae)
            }
        }

    @staticmethod
    def save_prediction(id_user, data):
        # 1. Convert dictionary shap_summary ke JSON string untuk disimpan di kolom Text
        shap_summary_str = json.dumps(data["shap_summary"]) if isinstance(data["shap_summary"], dict) else str(data["shap_summary"])

        # 2. Format data yang divalidasi ke format model riwayat prediksi
        history_data = {
            "id_user": id_user,
            "id_model": data["id_model"],
            "id_ml_model": data["id_ml_model"],
            "tahun": data["tahun"],
            "mileage": data["mileage"],
            "transmisi": data["transmisi"],
            "bahan_bakar": data["bahan_bakar"],
            "pajak": data["pajak"],
            "mpg": data["mpg"],
            "kapasitas_mesin": data["kapasitas_mesin"],
            "harga_prediksi": data["harga_prediksi"],
            "shap_summary": shap_summary_str
        }
        return PredictRepository.create(history_data)