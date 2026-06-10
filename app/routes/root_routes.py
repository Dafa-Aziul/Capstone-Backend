from flask import Blueprint

from app.utils.api_response import success_response

root_bp = Blueprint("root", __name__)


@root_bp.get("/")
def index():
    return success_response(
        message="Welcome to the backend API Prediksi Harga Mobil Bekas"
    )


@root_bp.get("/welcome")
def welcome():
    return success_response(
        message="Welcome endpoint is ready",
        data={
            "status": "ok",
        },
    )


@root_bp.get("/health")
def health():
    return success_response(
        message="API is running",
        data={
            "status": "healthy",
        },
    )
