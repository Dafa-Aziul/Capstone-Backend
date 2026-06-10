import logging
from flask import request
from marshmallow import ValidationError

from app.schemas.model_kendaraan_schema import (
    model_kendaraan_create,
    model_kendaraan_schema,
    model_kendaraan_update,
    model_kendaraans_schema,
)
from app.services.model_kendaraan_service import ModelKendaraanService
from app.utils.api_response import error_response, success_response

logger = logging.getLogger(__name__)

class ModelKendaraanController:
    @staticmethod
    def list_model_kendaraans():
        try:
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)
            search = request.args.get("search", None, type=str)

            result = ModelKendaraanService.get_all_model_kendaraans(
                page=page,
                per_page=per_page,
                search=search,
            )

            items_serialized = model_kendaraans_schema.dump(result["data"])

            return success_response(
                message="List model kendaraan berhasil diambil",
                data=items_serialized,
                meta=result["pagination"],
                status_code=200,
            )

        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil data model kendaraan",
                status_code=500,
            )

    @staticmethod
    def get_model_kendaraan_detail(id_model):
        try:
            model = ModelKendaraanService.get_model_kendaraan_by_id(id_model)
            model_data = model_kendaraan_schema.dump(model)

            return success_response(
                message="Detail model kendaraan berhasil diambil",
                data=model_data,
                status_code=200,
            )

        except ValueError as e:
            return error_response(message=str(e), status_code=404)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil detail model kendaraan",
                status_code=500,
            )

    @staticmethod
    def get_model_kendaraans_by_merek(id_merek):
        try:
            search = request.args.get("search", None, type=str)

            models = ModelKendaraanService.get_model_kendaraan_by_merek(
                id_merek=id_merek,
                search=search,
            )
            items_serialized = model_kendaraans_schema.dump(models)

            return success_response(
                message="List model kendaraan berdasarkan merek berhasil diambil",
                data=items_serialized,
                status_code=200,
            )

        except ValueError as e:
            return error_response(message=str(e), status_code=404)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil model kendaraan berdasarkan merek",
                status_code=500,
            )

    @staticmethod
    def create_model_kendaraan():
        try:
            data = request.get_json()
            if not data:
                return error_response(
                    message="Request body tidak boleh kosong",
                    status_code=400,
                )

            validated_data = model_kendaraan_create.load(data)
            model = ModelKendaraanService.create_model_kendaraan(
                id_merek=validated_data["id_merek"],
                nama_model=validated_data["nama_model"],
            )
            model_data = model_kendaraan_schema.dump(model)

            return success_response(
                message="Model kendaraan berhasil dibuat",
                data=model_data,
                status_code=201,
            )

        except ValidationError as e:
            return error_response(
                message="Validasi input gagal",
                errors=e.messages,
                status_code=400,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat membuat model kendaraan",
                status_code=500,
            )

    @staticmethod
    def update_model_kendaraan(id_model):
        try:
            data = request.get_json()
            if not data:
                return error_response(
                    message="Request body tidak boleh kosong",
                    status_code=400,
                )

            validated_data = model_kendaraan_update.load(data)
            model = ModelKendaraanService.update_model_kendaraan(
                id_model=id_model,
                id_merek=validated_data.get("id_merek"),
                nama_model=validated_data.get("nama_model"),
            )
            model_data = model_kendaraan_schema.dump(model)

            return success_response(
                message="Model kendaraan berhasil diupdate",
                data=model_data,
                status_code=200,
            )

        except ValidationError as e:
            return error_response(
                message="Validasi input gagal",
                errors=e.messages,
                status_code=400,
            )
        except ValueError as e:
            status_code = 404 if "tidak ditemukan" in str(e) else 400
            return error_response(message=str(e), status_code=status_code)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengupdate model kendaraan",
                status_code=500,
            )

    @staticmethod
    def delete_model_kendaraan(id_model):
        try:
            ModelKendaraanService.delete_model_kendaraan(id_model)

            return success_response(
                message="Model kendaraan berhasil dihapus",
                status_code=200,
            )

        except ValueError as e:
            return error_response(
                message=str(e),
                status_code=404 if "tidak ditemukan" in str(e) else 400,
            )
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat menghapus model kendaraan",
                status_code=500,
            )
