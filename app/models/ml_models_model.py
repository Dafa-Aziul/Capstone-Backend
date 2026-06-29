from app.extensions import db
from app.models.base import utc_now


class MlModel(db.Model):
    __tablename__ = "ml_models"

    id_ml_model = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uploaded_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id_user", onupdate="CASCADE"),
        nullable=False,
    )
    file_path = db.Column(db.String(150), unique=True, nullable=False)
    versi = db.Column(db.String(20), unique=True)
    r_squared = db.Column(db.Numeric(5, 4), nullable=False)
    mae = db.Column(db.Numeric(10, 2), nullable=False)
    is_current = db.Column(db.Boolean, nullable=False, default=True)
    uploaded_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    # Eager load user - model ML selalu perlu info who uploaded
    user = db.relationship("User", back_populates="ml_models", lazy="joined")
    # Lazy load predicts - prediksi bisa banyak, tidak selalu diakses
    predicts = db.relationship(
        "RiwayatPrediksi", back_populates="ml_model", lazy="subquery"
    )
