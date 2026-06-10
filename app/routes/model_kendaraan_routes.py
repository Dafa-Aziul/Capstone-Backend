from flask import Blueprint

from app.controllers.model_kendaraan_controller import ModelKendaraanController


model_kendaraan_bp = Blueprint(
    "model_kendaraan",
    __name__,
    url_prefix="/model-kendaraan",
)


@model_kendaraan_bp.get("")
def list_model_kendaraans():
    return ModelKendaraanController.list_model_kendaraans()


@model_kendaraan_bp.post("")
def create_model_kendaraan():
    return ModelKendaraanController.create_model_kendaraan()


@model_kendaraan_bp.get("/<int:id_model>")
def get_model_kendaraan_detail(id_model):
    return ModelKendaraanController.get_model_kendaraan_detail(id_model)


@model_kendaraan_bp.patch("/<int:id_model>")
def update_model_kendaraan(id_model):
    return ModelKendaraanController.update_model_kendaraan(id_model)


@model_kendaraan_bp.delete("/<int:id_model>")
def delete_model_kendaraan(id_model):
    return ModelKendaraanController.delete_model_kendaraan(id_model)


@model_kendaraan_bp.get("/merek/<int:id_merek>")
def get_model_kendaraans_by_merek(id_merek):
    return ModelKendaraanController.get_model_kendaraans_by_merek(id_merek)
