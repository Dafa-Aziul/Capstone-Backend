from app.extensions import db


class ModelKendaraan(db.Model):
    __tablename__ = "model_kendaraan"

    id_model = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_merek = db.Column(
        db.Integer,
        db.ForeignKey("merek.id_merek", onupdate="CASCADE"),
        nullable=False,
    )
    nama_model = db.Column(db.String(50), nullable=False)

    # Eager load merek - model kendaraan selalu perlu brand info
    merek = db.relationship("Merek", back_populates="model_kendaraans", lazy="joined")

    # Lazy load predicts - prediksi bisa banyak, jarang diakses dari model
    predicts = db.relationship(
        "RiwayatPrediksi", back_populates="model_kendaraan", lazy="subquery"
    )
