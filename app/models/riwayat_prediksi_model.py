from app.extensions import db
from app.models.base import utc_now


class RiwayatPrediksi(db.Model):
    __tablename__ = "riwayat_prediksi"

    id_riwayat = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(
        db.Integer,
        db.ForeignKey("users.id_user", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    id_model = db.Column(
        db.Integer,
        db.ForeignKey(
            "model_kendaraan.id_model", onupdate="CASCADE", ondelete="CASCADE"
        ),
        nullable=False,
    )
    id_ml_model = db.Column(
        db.Integer,
        db.ForeignKey("ml_models.id_ml_model", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    tahun = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    transmisi = db.Column(db.String(20), nullable=False)
    bahan_bakar = db.Column(db.String(20), nullable=False)
    pajak = db.Column(db.Integer, nullable=False)
    mpg = db.Column(db.Numeric(5, 2), nullable=False)
    kapasitas_mesin = db.Column(db.Numeric(3, 1), nullable=False)
    harga_prediksi = db.Column(db.Numeric(12, 2), nullable=False)
    shap_summary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    # Eager load relasi foreign keys - prediksi tidak lengkap tanpa data ini
    user = db.relationship("User", back_populates="predicts", lazy='joined')
    model_kendaraan = db.relationship("ModelKendaraan", back_populates="predicts", lazy='joined')
    ml_model = db.relationship("MlModel", back_populates="predicts", lazy='joined')
