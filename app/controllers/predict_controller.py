import logging
from flask import request, g
from marshmallow import ValidationError

from werkzeug.exceptions import BadRequest
from app.services.predict_service import PredictService
from app.schemas.predict_schema import predict_schema, save_prediction_schema
from app.utils.api_response import success_response, error_response

logger = logging.getLogger(__name__)


class PredictController:
    @staticmethod
    def predict_price():
        try:
            # 1. Validasi input JSON menggunakan Marshmallow
            json_data = request.get_json()
            if not json_data:
                return error_response(message="Request body JSON tidak boleh kosong.", status_code=400)
            
            validated_data = predict_schema.load(json_data)

            # 2. Panggil service untuk melakukan prediksi (tanpa perlu ID user)
            prediction_result = PredictService.predict(validated_data)

            # 3. Kembalikan response sukses
            return success_response(
                message="Prediksi harga mobil berhasil dibuat.",
                data=prediction_result,
                status_code=200
            )
            
        except BadRequest as e:
            return error_response(message=f"Format JSON tidak valid: {e.description}", status_code=400)
        except ValidationError as e:
            return error_response(message="Validasi input gagal.", errors=e.messages, status_code=400)
        except (ValueError, FileNotFoundError, RuntimeError) as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.error("Terjadi kesalahan saat prediksi: %s", str(e))
            return error_response(message="Terjadi kesalahan internal pada server saat melakukan prediksi.", status_code=500)

    @staticmethod
    def save_prediction():
        try:
            json_data = request.get_json()
            if not json_data:
                return error_response(message="Request body JSON tidak boleh kosong.", status_code=400)
            
            # Validasi input gabungan (parameter mobil + hasil prediksi + model_id + shap)
            validated_data = save_prediction_schema.load(json_data)

            if not hasattr(g, 'user'):
                return error_response(message="Akses ditolak: Anda harus login.", status_code=401)
            
            id_user = g.user.id_user

            # Eksekusi penyimpanan riwayat prediksi
            PredictService.save_prediction(id_user, validated_data)

            return success_response(
                message="Riwayat prediksi berhasil disimpan.",
                status_code=201
            )
            
        except ValidationError as e:
            return error_response(message="Validasi input gagal.", errors=e.messages, status_code=400)
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.error("Terjadi kesalahan saat menyimpan prediksi: %s", str(e))
            return error_response(message="Terjadi kesalahan internal pada server saat menyimpan riwayat prediksi.", status_code=500)