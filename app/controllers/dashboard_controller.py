import logging
from flask import request, g

from werkzeug.exceptions import BadRequest
from app.services.dashboard_service import DashboardService
from app.utils.api_response import success_response, error_response

logger = logging.getLogger(__name__)


class DashboardController:
    @staticmethod
    def stat_admin():
        try:
            stat = DashboardService.get_stat_admin()

            return success_response(
                message="Statistik Dashboard Admin berhasil diambil",
                data=stat,
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception(
                "Terjadi kesalahan saat mengambil stat dashboard: %s", str(e)
            )
            return error_response(
                message="Terjadi kesalahan di server saat mengambil statistik dashboard",
                status_code=500,
            )

    @staticmethod
    def stat_user():
        try:
            user_id = g.user.id_user

            stat = DashboardService.get_stat_user(id_user=user_id)

            return success_response(
                message="Statistik Dashboard User berhasil diambil",
                data=stat,
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception(
                "Terjadi kesalahan saat mengambil stat dashboard: %s", str(e)
            )
            return error_response(
                message="Terjadi kesalahan di server saat mengambil statistik dashboard",
                status_code=500,
            )

    @staticmethod
    def monthly_predict_admin():
        try:
            data = DashboardService.get_monthly_chart_admin()

            return success_response(
                message="Data Chart admin perbulan berhasil diambil",
                data=data,
                status_code=200,
            )

        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception(
                "Terjadi kesalahan saat mengambil data chart dashboard: %s", str(e)
            )
            return error_response(
                message="Terjadi kesalahan di server saat mengambil data chart dashboard",
                status_code=500,
            )

    @staticmethod
    def monthly_predict_user():
        try:
            user_id = g.user.id_user

            data = DashboardService.get_monthly_chart_user(id_user=user_id)

            return success_response(
                message="Data Chart user perbulan berhasil diambil",
                data=data,
                status_code=200,
            )
        except ValueError as e:
            return error_response(message=str(e), status_code=400)
        except Exception as e:
            logger.exception(
                "Terjadi kesalahan saat mengambil data chart dashboard: %s", str(e)
            )
            return error_response(
                message="Terjadi kesalahan di server saat mengambil data chart dashboard",
                status_code=500,
            )
