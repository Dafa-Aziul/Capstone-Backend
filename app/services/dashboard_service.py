from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.ml_models_repository import MlModelsRepository
from app.repositories.ml_models_repository import MlModel


class DashboardService:
    @staticmethod
    def get_stat_admin():
        stat = DashboardRepository.get_stat_admin()

        # 1. tambah versi Ml Model yang sedang aktif
        model_active, _ = MlModelsRepository.get_active_model()
        stat["model_active_version"] = model_active.versi if model_active else None

        return stat

    @staticmethod
    def get_stat_user(id_user):
        stat = DashboardRepository.get_stat_user(id_user)

        model_active, _ = MlModelsRepository.get_active_model()

        stat["acc"] = model_active.r_squared if model_active else None
        stat["model_active_version"] = model_active.versi if model_active else None

        return stat

    @staticmethod
    def get_monthly_chart_admin():
        return DashboardRepository.get_monthly_chart()

    @staticmethod
    def get_monthly_chart_user(id_user):
        return DashboardRepository.get_monthly_chart(id_user)
