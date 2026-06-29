from app.repositories.user_repository import UserRepository
from flask import current_app
from werkzeug.security import generate_password_hash


class UserService:
    @staticmethod
    def get_all(page=1, per_page=10, search=None):

        if page < 1:
            raise ValueError("Page harus >= 1")
        if per_page < 1 or per_page > 100:
            raise ValueError("Per page harus antara 1-100")

        item_not_organize, total, total_pages = UserRepository.get_all(
            page=page, per_page=per_page, search=search
        )

        return {
            "data": item_not_organize,
            "pagination": {
                "current_page": page,
                "per_page": per_page,
                "total_items": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
        }

    @staticmethod
    def set_status(target_user_id, current_user_id):
        if int(target_user_id) == int(current_user_id):
            raise ValueError("Tidak dapat update status sendiri")
        current_user = UserRepository.get_by_id(current_user_id)
        if not current_user:
            raise ValueError("User tidak ditemukan")
        return UserRepository.set_status_user(target_user_id, current_user.role)

    @staticmethod
    def get_stat():
        return UserRepository.get_stat()

    @staticmethod
    def create_admin(nama, email):
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            raise ValueError("Email sudah terdaftar")

        default_password = current_app.config.get("ADMIN_DEFAULT_PASSWORD")
        if not default_password:
            raise ValueError("ADMIN_DEFAULT_PASSWORD belum dikonfigurasi di environment")

        if len(default_password) < 6:
            raise ValueError("ADMIN_DEFAULT_PASSWORD minimal harus 6 karakter")

        hashed_password = generate_password_hash(default_password)
        return UserRepository.create(
            nama=nama,
            email=email,
            password=hashed_password,
            role="admin",
        )

    @staticmethod
    def reset_password(target_user_id, current_user_id):
        current_user = UserRepository.get_by_id(current_user_id)
        if not current_user:
            raise ValueError("User tidak ditemukan")

        default_password = current_app.config.get("USER_DEFAULT_PASSWORD")
        if not default_password:
            raise ValueError("USER_DEFAULT_PASSWORD belum dikonfigurasi di environment")

        if len(default_password) < 6:
            raise ValueError("USER_DEFAULT_PASSWORD minimal harus 6 karakter")

        hashed_password = generate_password_hash(default_password)
        return UserRepository.reset_password_user(
            id_user=target_user_id,
            hashed_password=hashed_password,
            actor_role=current_user.role,
        )

