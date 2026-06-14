from flask import Blueprint

from app.utils.api_response import success_response

root_bp = Blueprint("root", __name__)


@root_bp.get("/")
def index():
    return success_response(
        message="Welcome to the backend API Prediksi Harga Mobil Bekas"
    )
