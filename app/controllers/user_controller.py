import logging
from flask import request, g
from marshmallow import ValidationError

from app.schemas.user_schema import users_schema
from app.services.user_service import UserService
from app.utils.api_response import success_response, error_response

logger = logging.getLogger(__name__)

class UserController:
    @staticmethod
    def list_users():
        try:
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("per_page", 10, type=int)
            search = request.args.get("search", None, type=str)
            
            result = UserService.get_all(page=page, per_page=per_page, search=search)

            items_serialized = users_schema.dump(result["data"])
            
            return success_response(
                    message="List user berhasil diambil",
                    data=items_serialized,
                    meta=result["pagination"],
                    status_code=200,
                )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengambil data user",
                status_code=500,
            )
            
    @staticmethod
    def set_status_user(id_user):
        try:
            current_user_id = g.user.id_user
            user = UserService.set_status(target_user_id=id_user, current_user_id=current_user_id)
            
            status_text = "Aktif" if user.is_active else "Tidak Aktif"
            return success_response(
                message=f"Status User {user.nama} berhasil diubah menjadi {status_text}",
                status_code=200
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan saat mengubah status user",
                status_code=500,
            )
        
