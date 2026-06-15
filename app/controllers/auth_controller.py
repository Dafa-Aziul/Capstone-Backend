import logging
from flask import request, make_response
from marshmallow import ValidationError
from flask_jwt_extended import (
    set_access_cookies, 
    set_refresh_cookies, 
    unset_jwt_cookies,
    verify_jwt_in_request,
    get_jwt_identity
)

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
            logger.exception("Terjadi kesalahan saat register: %s", str(e))
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
            user, access_token, refresh_token = AuthService.login(
                email=validated_data["email"], password=validated_data["password"]
            )

            # Mempersiapkan response tanpa memunculkan access_token di body JSON
            resp_data = success_response(
                message="Login berhasil", data={"user": user.to_dict()}, status_code=200
            )
            response = make_response(resp_data)

            # Menyimpan kedua token di HTTP-Only Cookie
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)

            return response
        except ValidationError as e:
            return error_response(
                message="Validasi gagal", errors=e.messages, status_code=400
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=401)
        except Exception as e:
            logger.exception("Terjadi kesalahan saat login: %s", str(e))
            return error_response(
                message="Terjadi kesalahan server", errors=str(e), status_code=500
            )

    @staticmethod
    def refresh():
        try:
            # 1. Verifikasi keberadaan dan keabsahan refresh token di cookies
            verify_jwt_in_request(refresh=True, locations=["cookies"])
            current_user_id = get_jwt_identity()
            
            # 2. Panggil service untuk membuat access token baru
            new_access_token = AuthService.refresh_access_token(current_user_id)
            
            # 3. Siapkan response
            resp_data = success_response(message="Token berhasil diperbarui", status_code=200)
            response = make_response(resp_data)
            
            # 4. Timpa cookie access token lama dengan yang baru
            set_access_cookies(response, new_access_token)
            
            return response
            
        except ValueError as e:
            return error_response(message=str(e), status_code=401)
        except Exception as e:
            logger.exception("Terjadi kesalahan saat refresh token: %s", str(e))
            return error_response(
                message="Refresh token tidak valid atau telah berakhir. Silakan login kembali.", 
                errors=str(e), 
                status_code=401
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
            logger.exception("Terjadi kesalahan saat logout: %s", str(e))
            return error_response(
                message="Terjadi kesalahan server", errors=str(e), status_code=500
            )
