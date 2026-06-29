from flask import Blueprint
from app.middlewares.auth_middleware import login_required, role_required
from app.controllers.model_kendaraan_controller import ModelKendaraanController

model_kendaraan_bp = Blueprint(
    "model_kendaraan",
    __name__,
    url_prefix="/model-kendaraan",
)


@model_kendaraan_bp.get("")
@login_required
def list_model_kendaraans():
    return ModelKendaraanController.list_model_kendaraans()


@model_kendaraan_bp.get("/<int:id_model>")
@login_required
def get_model_kendaraan_detail(id_model):
    return ModelKendaraanController.get_model_kendaraan_detail(id_model)


@model_kendaraan_bp.get("/<int:id_merek>/merek")
@login_required
def get_model_kendaraans_by_merek(id_merek):
    return ModelKendaraanController.get_model_kendaraans_by_merek(id_merek)


@model_kendaraan_bp.post("")
@login_required
@role_required('admin')
def create_model_kendaraan():
    return ModelKendaraanController.create_model_kendaraan()


@model_kendaraan_bp.put("/<int:id_model>")
@login_required
@role_required('admin')
def update_model_kendaraan(id_model):
    return ModelKendaraanController.update_model_kendaraan(id_model)


@model_kendaraan_bp.delete("/<int:id_model>")
@login_required
@role_required('admin')
def delete_model_kendaraan(id_model):
    return ModelKendaraanController.delete_model_kendaraan(id_model)
