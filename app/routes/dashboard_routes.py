from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController
from app.middlewares.auth_middleware import login_required, role_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.get("/stat/admin")
@login_required
@role_required("admin")
def get_stat_admin():
    return DashboardController.stat_admin()


@dashboard_bp.get("/stat/user")
@login_required
@role_required("user")
def get_stat_user():
    return DashboardController.stat_user()


@dashboard_bp.get("/chart/admin")
@login_required
@role_required("admin")
def get_chart_admin():
    return DashboardController.monthly_predict_admin()


@dashboard_bp.get("/chart/user")
@login_required
@role_required("user")
def get_chart_user():
    return DashboardController.monthly_predict_user()
