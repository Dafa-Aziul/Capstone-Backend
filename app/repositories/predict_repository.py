from app.extensions import db
from app.models.riwayat_prediksi_model import RiwayatPrediksi
from sqlalchemy.orm import joinedload
from sqlalchemy import or_, func, extract
from app.models.user_model import User
from app.models.model_kendaraan_model import ModelKendaraan
from app.models.merek_model import Merek
from app.models.base import utc_now
from datetime import timedelta


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
    def get_stat_predict_admin():
        total_predict = RiwayatPrediksi.query.count()
        current_date = utc_now()

        total_predict_today = RiwayatPrediksi.query.filter(
            extract("year", RiwayatPrediksi.created_at) == current_date.year,
            extract("month", RiwayatPrediksi.created_at) == current_date.month,
            extract("day", RiwayatPrediksi.created_at) == current_date.day,
        ).count()

        return {
            "total_predict": total_predict,
            "total_predict_today": total_predict_today,
        }

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
            joinedload(RiwayatPrediksi.model_kendaraan),
        ).filter(RiwayatPrediksi.id_user == user_id)

        if search:
            query = query.outerjoin(ModelKendaraan.merek).filter(
                or_(
                    ModelKendaraan.nama_model.ilike(f"%{search}%"),
                    Merek.nama_merek.ilike(f"%{search}%"),
                )
            )

        query = query.order_by(RiwayatPrediksi.created_at.desc())

        paginate = query.paginate(page=page, per_page=per_page, error_out=False)

        return paginate.items, paginate.total, paginate.pages

    @staticmethod
    def get_stat_predict_user(user_id):
        # 1. Total Prediksi
        total_predict = RiwayatPrediksi.query.filter_by(id_user=user_id).count()

        # 2. Rata-rata harga prediksi
        avg_predict_price = (
            db.session.query(func.avg(RiwayatPrediksi.harga_prediksi))
            .filter_by(id_user=user_id)
            .scalar()
        )
        avg_predict_price = float(avg_predict_price) if avg_predict_price else 0.0

        # 3. Total prediksi bulan ini
        current_date = utc_now()
        total_predict_permonth = RiwayatPrediksi.query.filter(
            RiwayatPrediksi.id_user == user_id,
            extract("year", RiwayatPrediksi.created_at) == current_date.year,
            extract("month", RiwayatPrediksi.created_at) == current_date.month,
        ).count()

        total_predict_today = RiwayatPrediksi.query.filter(
            RiwayatPrediksi.id_user == user_id,
            extract("year", RiwayatPrediksi.created_at) == current_date.year,
            extract("month", RiwayatPrediksi.created_at) == current_date.month,
            extract("day", RiwayatPrediksi.created_at) == current_date.day,
        ).count()

        return {
            "total_predict": total_predict,
            "avg_predict_price": avg_predict_price,
            "total_predict_this_month": total_predict_permonth,
            "total_predict_today": total_predict_today,
        }

    @staticmethod
    def delete(id_riwayat):
        RiwayatPrediksi.query.filter_by(id_riwayat=id_riwayat).delete()
        db.session.commit()

        return True

    @staticmethod
    def get_weekly_chart(user_id=None):
        end_date = utc_now()
        # Set ke awal hari 6 hari yang lalu untuk mencakup 7 hari penuh (termasuk hari ini)
        start_date = (end_date - timedelta(days=6)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        query = RiwayatPrediksi.query.filter(RiwayatPrediksi.created_at >= start_date)

        if user_id:
            query = query.filter(RiwayatPrediksi.id_user == user_id)

        records = query.all()

        # Siapkan dictionary untuk 7 hari terakhir (default value 0)
        date_counts = {}
        for i in range(7):
            current_day = start_date + timedelta(days=i)
            date_str = current_day.strftime("%Y-%m-%d")
            date_counts[date_str] = 0

        for record in records:
            record_date = record.created_at.strftime("%Y-%m-%d")
            if record_date in date_counts:
                date_counts[record_date] += 1

        # Ubah menjadi format array of object untuk frontend
        return [{"date": k, "value": v} for k, v in date_counts.items()]

    @staticmethod
    def get_lastest_activity(user_id=None, jumlah=3):
        query = RiwayatPrediksi.query.options(
            joinedload(RiwayatPrediksi.user),
            joinedload(RiwayatPrediksi.model_kendaraan).joinedload(
                ModelKendaraan.merek
            ),
            joinedload(RiwayatPrediksi.ml_model),
        )

        query = query.order_by(RiwayatPrediksi.created_at.desc())

        if user_id:
            query = query.filter(RiwayatPrediksi.id_user == user_id)

        if jumlah:
            query = query.limit(jumlah)

        return query.all()
