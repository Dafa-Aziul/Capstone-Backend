from flask import Blueprint

from app.controllers.user_controller import UserController
from app.middlewares.auth_middleware import login_required, role_required

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.get("")
@login_required
@role_required("admin")
def list_user():
    return UserController.list_users()


@user_bp.patch("/<int:id_user>/set-status")
@login_required
@role_required("admin")
def update_status(id_user):
    return UserController.set_status_user(id_user)


@user_bp.get("/stats")
@login_required
@role_required("admin")
def get_user_stats():
    return UserController.get_user_stats()
