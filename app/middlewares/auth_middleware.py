from functools import wraps
from flask import g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.utils.api_response import error_response
from app.repositories.user_repository import UserRepository


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Secara eksplisit mengecek token di dalam cookies
            verify_jwt_in_request(locations=["cookies"])
            
            # Mengambil identity (id_user) dari payload token
            user_id = get_jwt_identity()
            
            # Cek ke database apakah user masih ada/valid
            user = UserRepository.get_by_id(int(user_id))
            if not user:
                return error_response(
                    message="Akses ditolak: User tidak ditemukan", 
                    status_code=401
                )
            
            # Pastikan user masih berstatus aktif
            if not user.is_active:
                return error_response(
                    message="Akses ditolak: Akun Anda telah dinonaktifkan", 
                    status_code=403
                )
            
            g.user = user
            
            return fn(*args, **kwargs)
            
        except Exception as e:
            return error_response(
                message="Akses ditolak: Sesi tidak valid atau telah berakhir", 
                errors=str(e), 
                status_code=401
            )
            
    return wrapper


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Pastikan user sudah melewati login_required (g.user sudah ada)
            if not hasattr(g, 'user'):
                return error_response(
                    message="Akses ditolak: Anda harus login terlebih dahulu", 
                    status_code=401
                )
            
            # Cek apakah role user saat ini termasuk di dalam daftar allowed_roles
            if g.user.role not in allowed_roles:
                return error_response(
                    message="Akses ditolak: Anda tidak memiliki izin untuk aksi ini", 
                    status_code=403
                )
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator