import logging
from flask import request
from app.services.merek_service import MerekService
from app.schemas.merek_schema import merek_schema, mereks_schema, merek_create_schema
from app.utils.api_response import success_response, error_response
from marshmallow import ValidationError

logger = logging.getLogger(__name__)

class MerekController:
    @staticmethod
    def list_mereks():
        try:
            # Get query parameters
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)
            search = request.args.get("search", None, type=str)

            # Get data dari service
            result = MerekService.get_all_mereks(
                page=page, per_page=per_page, search=search
            )

            # Serialize items
            items_serialized = mereks_schema.dump(result["data"])

            # Format response
            return success_response(
                message="List merek berhasil diambil",
                data=items_serialized,
                meta=result["pagination"],
                status_code=200,
            )

        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil data merek",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def get_merek_detail(id_merek):
        try:
            merek = MerekService.get_merek_by_id(id_merek)
            merek_data = merek_schema.dump(merek)

            return success_response(
                message="Detail merek berhasil diambil",
                data=merek_data,
                status_code=200,
            )

        except ValueError as e:
            return error_response(message=str(e), status_code=404)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil detail merek",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def create_merek():
        try:
            # Get JSON data
            data = request.get_json()
            if not data:
                return error_response(
                    message="Request body tidak boleh kosong", status_code=400
                )

            # Validasi input dengan schema
            validated_data = merek_create_schema.load(data)

            # Create merek via service
            merek = MerekService.create_merek(validated_data["nama_merek"])
            merek_data = merek_schema.dump(merek)

            return success_response(
                message="Merek berhasil dibuat",
                data=merek_data,
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
                message="Terjadi kesalahan saat membuat merek",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def update_merek(id_merek):
        try:
            # Get JSON data
            data = request.get_json()
            if not data:
                return error_response(
                    message="Request body tidak boleh kosong", status_code=400
                )

            # Validasi input
            validated_data = merek_create_schema.load(data)

            # Update merek via service
            merek = MerekService.update_merek(id_merek, validated_data["nama_merek"])
            merek_data = merek_schema.dump(merek)

            return success_response(
                message="Merek berhasil diupdate",
                data=merek_data,
                status_code=200,
            )

        except ValidationError as e:
            return error_response(
                message="Validasi input gagal", errors=e.messages, status_code=400
            )
        except ValueError as e:
            return error_response(
                message=str(e), status_code=404 if "tidak ditemukan" in str(e) else 400
            )
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengupdate merek",
                errors=str(e),
                status_code=500,
            )

    @staticmethod
    def delete_merek(id_merek):
        try:
            MerekService.delete_merek(id_merek)

            return success_response(message="Merek berhasil dihapus", status_code=200)

        except ValueError as e:
            error_msg = str(e)
            if "tidak ditemukan" in error_msg:
                status = 404
            elif "Tidak bisa hapus" in error_msg:
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
