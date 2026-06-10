import logging
from flask import request, g
from marshmallow import ValidationError
from app.services.ml_models_service import MlModelsService
from app.schemas.ml_models_schema import (
    ml_model_schema,
    ml_models_schema,
    ml_model_create_schema,
)
from app.utils.api_response import success_response, error_response


logger = logging.getLogger(__name__)

class MlModelsController:

    @staticmethod
    def list_all():
        try:
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)
            search = request.args.get("search", None, type=str)

            result = MlModelsService.get_all(
                page=page, per_page=per_page, search=search
            )

            items_serialized = ml_models_schema.dump(result["items"])

            return success_response(
                message="Daftar model ML berhasil diambil",
                data={
                    "ml_models": items_serialized,
                    "pagination": result["pagination"],
                },
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil daftar model ML",
                status_code=500,
            )

    @staticmethod
    def get_detail(id_ml_model):
        try:
            model = MlModelsService.get_by_id(id_ml_model)

            return success_response(
                message="Detail model ML berhasil diambil",
                data={"ml_model": ml_model_schema.dump(model)},
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=404)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan di server", 
                status_code=500
            )

    @staticmethod
    def create():
        try:
            # Gabungkan data form dan file untuk divalidasi oleh Marshmallow
            input_data = request.form.to_dict()
            if "file" in request.files and request.files["file"].filename:
                input_data["file"] = request.files.get("file")
                
            validated_data = ml_model_create_schema.load(input_data)
            
            if not hasattr(g, "user"):
                return error_response(
                    message="Akses ditolak: Sesi tidak valid", status_code=401
                )

            uploaded_by = g.user.id_user

            record = MlModelsService.create(
                uploaded_by=uploaded_by,
                file=validated_data["file"],
                versi=validated_data["versi"],
                r_squared=validated_data["r_squared"],
                mae=validated_data["mae"],
            )

            return success_response(
                message="Model ML berhasil diunggah dan disimpan",
                data={"ml_model": ml_model_schema.dump(record)},
                status_code=201,
            )
        except ValidationError as e:
            return error_response(
                message="Validasi input gagal", errors=e.messages, status_code=400
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat menyimpan model",
                status_code=500,
            )

    @staticmethod
    def set_active(id_ml_model):
        try:
            record = MlModelsService.set_active(id_ml_model)

            return success_response(
                message="Model ML berhasil diaktifkan",
                data={"ml_model": ml_model_schema.dump(record)},
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=404)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengaktifkan model",
                status_code=500,
            )

    @staticmethod
    def delete(id_ml_model):
        try:
            MlModelsService.delete(id_ml_model)

            return success_response(
                message="Model ML berhasil dihapus",
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=404)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat menghapus model",
                status_code=500,
            )
