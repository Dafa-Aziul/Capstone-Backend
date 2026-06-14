from app.extensions import db
from app.models.riwayat_prediksi_model import RiwayatPrediksi
from app.models.ml_models_model import MlModel
from app.models.user_model import User
from app.models.base import utc_now
from datetime import timedelta


class DashboardRepository:
    @staticmethod
    def get_stat_admin():
        total_predict = RiwayatPrediksi.query.count()
        total_user = User.query.count()
        total_active = User.query.filter_by(is_active=True).count()

        return {
            "total_predict": total_predict,
            "total_user": total_user,
            "total_active": total_active,
        }

    @staticmethod
    def get_stat_user(id_user):
        total_predict = RiwayatPrediksi.query.filter_by(id_user=id_user).count()
        last_predict = (
            RiwayatPrediksi.query.filter_by(id_user=id_user)
            .order_by(RiwayatPrediksi.created_at.desc())
            .first()
        )

        return {
            "total_predict": total_predict,
            "last_predict": last_predict.harga_prediksi if last_predict else None,
        }

    @staticmethod
    def get_monthly_chart(user_id=None):
        end_date = utc_now()

        # Siapkan dictionary untuk 5 bulan terakhir (default value 0)
        month_counts = {}
        start_date = None

        # Iterasi mundur dari 4 bulan yang lalu sampai bulan ini (total 5 bulan)
        for i in range(4, -1, -1):
            y = end_date.year
            m = end_date.month - i
            while m <= 0:
                m += 12
                y -= 1

            month_str = f"{y}-{m:02d}"
            month_counts[month_str] = 0

            # Ambil tanggal 1 di bulan yang paling awal (4 bulan lalu)
            if i == 4:
                start_date = end_date.replace(
                    year=y, month=m, day=1, hour=0, minute=0, second=0, microsecond=0
                )

        query = RiwayatPrediksi.query.filter(RiwayatPrediksi.created_at >= start_date)

        if user_id:
            query = query.filter(RiwayatPrediksi.id_user == user_id)

        records = query.all()

        for record in records:
            record_month = record.created_at.strftime("%Y-%m")
            if record_month in month_counts:
                month_counts[record_month] += 1

        # Ubah menjadi format array of object untuk frontend
        return [{"date": k, "value": v} for k, v in month_counts.items()]
