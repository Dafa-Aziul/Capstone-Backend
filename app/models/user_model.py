from app.extensions import db
from app.models.base import utc_now


class User(db.Model):
    __tablename__ = "users"

    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    role = db.Column(
        db.Enum("superadmin", "admin", "user", name="user_roles"),
        nullable=False,
        default="user",
    )
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)

    # Hindari cascade delete untuk menjaga data historis tetap utuh.
    ml_models = db.relationship("MlModel", back_populates="user", lazy=True)
    predicts = db.relationship("RiwayatPrediksi", back_populates="user", lazy=True)

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "nama": self.nama,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
