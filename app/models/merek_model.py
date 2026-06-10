from app.extensions import db
from app.models.base import utc_now


class Merek(db.Model):
    __tablename__ = "merek"

    id_merek = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_merek = db.Column(db.String(30), unique=True, nullable=False)

    model_kendaraans = db.relationship("ModelKendaraan", back_populates="merek", lazy=True)
