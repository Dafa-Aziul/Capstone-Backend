from app.extensions import db
from app.models.riwayat_prediksi_model import RiwayatPrediksi


class PredictRepository:
    @staticmethod
    def create(data):
        record = RiwayatPrediksi(**data)
        db.session.add(record)
        db.session.commit()
        return record