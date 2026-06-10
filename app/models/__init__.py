from app.models.base import BaseModel, TimestampMixin
from app.models.user_model import User
from app.models.merek_model import Merek
from app.models.ml_models_model import MlModel
from app.models.model_kendaraan_model import ModelKendaraan
from app.models.riwayat_prediksi_model import RiwayatPrediksi

__all__ = ["BaseModel", "TimestampMixin", "User", "Merek", "MlModel", "ModelKendaraan", "RiwayatPrediksi"]
