from flask import Blueprint

from app.controllers.user_controller import UserController
from app.middlewares.auth_middleware import login_required, role_required

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.post("/admin")
@login_required
@role_required("superadmin")
def create_admin():
    return UserController.create_admin()


@user_bp.get("")
@login_required
@role_required("superadmin")
def list_user():
    return UserController.list_users()


@user_bp.patch("/<int:id_user>/set-status")
@login_required
@role_required("superadmin")
def update_status(id_user):
    return UserController.set_status_user(id_user)


@user_bp.patch("/<int:id_user>/reset-password")
@login_required
@role_required("superadmin")
def reset_password(id_user):
    return UserController.reset_password_user(id_user)


@user_bp.get("/stats")
@login_required
@role_required("superadmin")
def get_user_stats():
    return UserController.get_user_stats()
