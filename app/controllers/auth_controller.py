import logging
from flask import request, make_response
from marshmallow import ValidationError
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies

from app.services.auth_service import AuthService
from app.schemas.auth_schema import login_schema, register_schema
from app.utils.api_response import success_response, error_response

logger = logging.getLogger(__name__)


class AuthController:

    @staticmethod
    def register():
        try:
            data = request.get_json()
            if not data:
                return error_response(
                    message="Request body is required", status_code=400
                )

            validated_data = register_schema.load(data)
            user = AuthService.register(
                nama=validated_data["nama"],
                email=validated_data["email"],
                password=validated_data["password"],
            )

            return success_response(
                message="Registrasi berhasil",
                data={"user": user.to_dict()},
                status_code=201,
            )
        except ValidationError as e:
            return error_response(
                message="Validasi gagal", errors=e.messages, status_code=400
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan server", errors=str(e), status_code=500
            )

    @staticmethod
    def login():
        try:
            data = request.get_json()
            if not data:
                return error_response(
                    message="Request body is required", status_code=400
                )

            validated_data = login_schema.load(data)
            user, token = AuthService.login(
                email=validated_data["email"], password=validated_data["password"]
            )

            # Mempersiapkan response tanpa memunculkan access_token di body JSON
            resp_data = success_response(
                message="Login berhasil", data={"user": user.to_dict()}, status_code=200
            )
            response = make_response(resp_data)

            # Menyimpan token di HTTP-Only Cookie
            set_access_cookies(response, token)

            return response
        except ValidationError as e:
            return error_response(
                message="Validasi gagal", errors=e.messages, status_code=400
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=401)
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan server", errors=str(e), status_code=500
            )

    @staticmethod
    def logout():
        try:
            resp_data = success_response(message="Logout berhasil", status_code=200)
            response = make_response(resp_data)

            # Menghapus token dari cookie
            unset_jwt_cookies(response)
            return response
        except Exception as e:
            logger.exception("Terjadi kesalahan: %s", str(e))
            return error_response(
                message="Terjadi kesalahan server", errors=str(e), status_code=500
            )
