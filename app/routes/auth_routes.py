from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    return AuthController.register()


@auth_bp.post("/login")
def login():
    return AuthController.login()


@auth_bp.post("/logout")
def logout():
    return AuthController.logout()


@auth_bp.post("/refresh")
def refresh():
    return AuthController.refresh()
