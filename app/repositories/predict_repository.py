from app.extensions import db
from app.models.riwayat_prediksi_model import RiwayatPrediksi
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from app.models.user_model import User
from app.models.model_kendaraan_model import ModelKendaraan
from app.models.merek_model import Merek


class PredictRepository:
    @staticmethod
    def create(data):
        record = RiwayatPrediksi(**data)
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def get_all(page=1, per_page=10, search=None):
        query = RiwayatPrediksi.query.options(
            joinedload(RiwayatPrediksi.user),
            joinedload(RiwayatPrediksi.model_kendaraan),
            joinedload(RiwayatPrediksi.ml_model),
        )

        if search:
            query = (
                query.outerjoin(RiwayatPrediksi.user)
                .outerjoin(RiwayatPrediksi.model_kendaraan)
                .outerjoin(ModelKendaraan.merek)
                .filter(
                    or_(
                        User.email.ilike(f"%{search}%"),
                        ModelKendaraan.nama_model.ilike(f"%{search}%"),
                        Merek.nama_merek.ilike(f"%{search}%"),
                    )
                )
            )

        query = query.order_by(RiwayatPrediksi.created_at)

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return paginated.items, paginated.total, paginated.pages

    @staticmethod
    def get_by_id(id_riwayat):
        return RiwayatPrediksi.query.options(
            joinedload(RiwayatPrediksi.model_kendaraan).joinedload(
                ModelKendaraan.merek
            ),
            joinedload(RiwayatPrediksi.ml_model),
        ).get(id_riwayat)
        
        

    @staticmethod
    def get_predict_by_user(user_id, page=1, per_page=10, search=None):
        query = RiwayatPrediksi.query.options(
            joinedload(RiwayatPrediksi.user),
            joinedload(RiwayatPrediksi.ml_model),
            joinedload(RiwayatPrediksi.model_kendaraan).joinedload(
                ModelKendaraan.merek
            ),
        ).filter(RiwayatPrediksi.id_user == user_id)

        if search:
            query = (
                query.outerjoin(RiwayatPrediksi.model_kendaraan)
                .outerjoin(ModelKendaraan.merek)
                .filter(
                    or_(
                        ModelKendaraan.nama_model.ilike(f"%{search}%"),
                        Merek.nama_merek.ilike(f"%{search}%"),
                    )
                )
            )

        query = query.order_by(RiwayatPrediksi.created_at.desc())

        paginate = query.paginate(page=page, per_page=per_page, error_out=False)

        return paginate.items, paginate.total, paginate.pages


    @staticmethod
    def delete(id_riwayat):
        RiwayatPrediksi.query.filter_by(id_riwayat=id_riwayat).delete()
        db.session.commit()
        
        return True