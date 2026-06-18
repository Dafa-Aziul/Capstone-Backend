import logging
from flask import request, g
from marshmallow import ValidationError

from werkzeug.exceptions import BadRequest
from app.services.predict_service import PredictService
from app.schemas.predict_schema import (
    predict_schema,
    save_prediction_schema,
    predicts_schema,
    predict_by_user_schema,
    predict_detail_schema,
)
from app.utils.api_response import success_response, error_response

logger = logging.getLogger(__name__)


class PredictController:
    @staticmethod
    def list_predict():
        try:
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)
            search = request.args.get("search", None, type=str)

            result = PredictService.get_all_predict(
                page=page, per_page=per_page, search=search
            )

            items_serialized = predicts_schema.dump(result["data"])

            return success_response(
                message="List Predict berhasil diambil",
                data=items_serialized,
                meta=result["pagination"],
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil data Riwayat Prediksi",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def list_predics_by_user():
        try:
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)
            search = request.args.get("search", None, type=str)

            if not hasattr(g, "user"):
                return error_response(
                    message="Akses ditolak: Anda harus login.", status_code=401
                )

            id_user = g.user.id_user

            result = PredictService.get_predict_by_user(
                id_user=id_user, page=page, per_page=per_page, search=search
            )

            items_serialized = predict_by_user_schema.dump(result["data"])

            return success_response(
                message="List Predict by user berhasil diambil",
                data=items_serialized,
                meta=result["pagination"],
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil data Riwayat Prediksi",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def get_stat_user():
        try:
            # Mengambil ID user dari konteks login JWT
            user_id = g.user.id_user

            stats = PredictService.get_stat_predict_user(user_id)

            return success_response(
                message="Statistik prediksi user berhasil diambil",
                data=stats,
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception(
                "Terjadi kesalahan saat mengambil stat prediksi: %s", str(e)
            )
            return error_response(
                message="Terjadi kesalahan di server saat mengambil statistik prediksi",
                status_code=500,
            )

    @staticmethod
    def get_stat_admin():
        try:
            stats = PredictService.get_stat_predict_admin()

            return success_response(
                message="Statistik prediksi admin berhasil diambil",
                data=stats,
                status_code=200,
            )
        except Exception as e:
            logger.exception(
                "Terjadi kesalahan saat mengambil stat prediksi admin: %s", str(e)
            )
            return error_response(
                message="Terjadi kesalahan di server saat mengambil statistik prediksi admin",
                status_code=500,
            )

    @staticmethod
    def get_chart_admin():
        try:
            data = PredictService.get_weekly_chart_admin()
            
            return success_response(
                message="Data chart mingguan admin berhasil diambil",
                data=data,
                status_code=200,
            )
        except Exception as e:
            logger.exception(
                "Terjadi kesalahan saat mengambil chart admin: %s", str(e)
            )
            return error_response(
                message="Terjadi kesalahan di server saat mengambil data chart",
                status_code=500,
            )

    @staticmethod
    def detail_riwayat(id_riwayat):
        try:
            riwayat = PredictService.get_riwayat_by_id(id_riwayat)

            # Ubah objek riwayat dari DB menjadi dictionary (format JSON) menggunakan schema
            riwayat_data = predict_detail_schema.dump(riwayat)

            return success_response(
                message="Detail Riwayat berhasil diambil",
                data=riwayat_data,
                status_code=200,
            )

        except ValueError as e:
            return error_response(message=str(e), status_code=404)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil detail riwayat prediksi",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def predict_price():
        try:
            # 1. Validasi input JSON menggunakan Marshmallow
            json_data = request.get_json()
            if not json_data:
                return error_response(
                    message="Request body JSON tidak boleh kosong.", status_code=400
                )

            validated_data = predict_schema.load(json_data)

            # 2. Panggil service untuk melakukan prediksi (tanpa perlu ID user)
            prediction_result = PredictService.predict(validated_data)

            # 3. Kembalikan response sukses
            return success_response(
                message="Prediksi harga mobil berhasil dibuat.",
                data=prediction_result,
                status_code=200,
            )

        except BadRequest as e:
            return error_response(
                message=f"Format JSON tidak valid: {e.description}", status_code=400
            )
        except ValidationError as e:
            return error_response(
                message="Validasi input gagal.", errors=e.messages, status_code=400
            )
        except (ValueError, FileNotFoundError, RuntimeError) as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.error("Terjadi kesalahan saat prediksi: %s", str(e))
            return error_response(
                message="Terjadi kesalahan internal pada server saat melakukan prediksi.",
                status_code=500,
            )

    @staticmethod
    def save_prediction():
        try:
            json_data = request.get_json()
            if not json_data:
                return error_response(
                    message="Request body JSON tidak boleh kosong.", status_code=400
                )

            # Validasi input gabungan (parameter mobil + hasil prediksi + model_id + shap)
            validated_data = save_prediction_schema.load(json_data)

            if not hasattr(g, "user"):
                return error_response(
                    message="Akses ditolak: Anda harus login.", status_code=401
                )

            id_user = g.user.id_user

            # Eksekusi penyimpanan riwayat prediksi
            PredictService.save_prediction(id_user, validated_data)

            return success_response(
                message="Riwayat prediksi berhasil disimpan.", status_code=201
            )

        except ValidationError as e:
            return error_response(
                message="Validasi input gagal.", errors=e.messages, status_code=400
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.error("Terjadi kesalahan saat menyimpan prediksi: %s", str(e))
            return error_response(
                message="Terjadi kesalahan internal pada server saat menyimpan riwayat prediksi.",
                status_code=500,
            )

    @staticmethod
    def delete_riwayat(id_riwayat):
        try:
            current_user_id = g.user.id_user

            PredictService.delete_riwayat(id_riwayat, current_user_id=current_user_id)

            return success_response(message="Riwayat berhasil dihapus", status_code=200)
        except ValueError as e:
            error_msg = str(e)
            if "tidak ditemukan" in error_msg:
                status = 404
            elif "Tidak dapat" in error_msg:
                status = 409
            else:
                status = 400

            return error_response(message=error_msg, status_code=status)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat menghapus merek",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def get_latest_activity():
        try:
            jumlah = request.args.get("jumlah", 5, type=int)
            activities = PredictService.get_latest_activity(jumlah)

            items_serialized = predicts_schema.dump(activities)

            return success_response(
                message="Aktivitas terbaru berhasil diambil",
                data=items_serialized,
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil aktivitas terbaru",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def get_latest_activity_user():
        try:
            jumlah = request.args.get("jumlah", 5, type=int)
            id_user = g.user.id_user
            activities = PredictService.get_latest_activity_user(id_user, jumlah)

            items_serialized = predicts_schema.dump(activities)

            return success_response(
                message="Aktivitas terbaru user berhasil diambil",
                data=items_serialized,
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil aktivitas terbaru user",
                errors=str(e),
                status_code=500,
            )
