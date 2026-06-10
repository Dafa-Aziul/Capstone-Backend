from flask import Blueprint
from app.controllers.predict_controller import PredictController
from app.middlewares.auth_middleware import login_required

predict_bp = Blueprint('predict', __name__, url_prefix='/predict')

@predict_bp.post('')
@login_required
def predict_price():
    return PredictController.predict_price()

@predict_bp.post('/save')
@login_required
def save_prediction():
    return PredictController.save_prediction()