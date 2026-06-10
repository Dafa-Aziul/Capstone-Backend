from datetime import datetime, timezone

from sqlalchemy import event

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utc_now)


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def to_dict(self):
        result = {}

        for column in self.__table__.columns:
            value = getattr(self, column.name)

            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value

        return result


@event.listens_for(BaseModel, "before_update", propagate=True)
def receive_before_update(mapper, connection, target):
    if hasattr(target, "updated_at"):
        target.updated_at = utc_now()
