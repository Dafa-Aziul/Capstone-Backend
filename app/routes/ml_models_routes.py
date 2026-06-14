from flask import Blueprint
from app.controllers.ml_models_controller import MlModelsController
from app.middlewares.auth_middleware import login_required, role_required

ml_models_bp = Blueprint("ml_models", __name__, url_prefix="/ml-model")


@ml_models_bp.get("")
@login_required
@role_required("admin")
def list_all():
    return MlModelsController.list_all()


@ml_models_bp.get("/active")
@login_required
@role_required("admin")
def get_active_model():
    return MlModelsController.get_model_active()


@ml_models_bp.get("/<int:id_ml_model>")
@login_required
@role_required("admin")
def get_detail(id_ml_model):
    return MlModelsController.get_detail(id_ml_model)


@ml_models_bp.post("")
@login_required
@role_required("admin")
def create():
    return MlModelsController.create()


@ml_models_bp.patch("/<int:id_ml_model>/active")
@login_required
@role_required("admin")
def set_active(id_ml_model):
    return MlModelsController.set_active(id_ml_model)


@ml_models_bp.delete("/<int:id_ml_model>")
@login_required
@role_required("admin")
def delete(id_ml_model):
    return MlModelsController.delete(id_ml_model)
