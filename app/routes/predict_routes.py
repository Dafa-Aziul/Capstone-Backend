from flask import Blueprint
from app.controllers.predict_controller import PredictController
from app.middlewares.auth_middleware import login_required, role_required

predict_bp = Blueprint("predict", __name__, url_prefix="/predict")


@predict_bp.get("")
@login_required
@role_required("admin")
def list_predicts():
    return PredictController.list_predict()


@predict_bp.get("/stat/admin")
@login_required
@role_required("admin")
def get_stat_admin():
    return PredictController.get_stat_admin()


@predict_bp.get("/chart/admin")
@login_required
@role_required("admin")
def get_chart_admin():
    return PredictController.get_chart_admin()


@predict_bp.get("/by-user")
@login_required
@role_required('user')
def list_predict_by_user():
    return PredictController.list_predics_by_user()


@predict_bp.get("/stat/user")
@login_required
@role_required('user')
def get_stat_user():
    return PredictController.get_stat_user()


@predict_bp.post("")
@login_required
@role_required('user')
def predict_price():
    return PredictController.predict_price()


@predict_bp.post("/save")
@login_required
@role_required('user')
def save_prediction():
    return PredictController.save_prediction()


@predict_bp.get("/<int:id_riwayat>")
@login_required
@role_required('user')
def get_detail_riwayat(id_riwayat):
    return PredictController.detail_riwayat(id_riwayat)


@predict_bp.delete("/<int:id_riwayat>")
@login_required
@role_required('user')
def delete_riwayat(id_riwayat):
    return PredictController.delete_riwayat(id_riwayat)


@predict_bp.get("/latest-activity/admin")
@login_required
@role_required("admin")
def get_latest_activity():
    return PredictController.get_latest_activity()


@predict_bp.get("/latest-activity/user")
@login_required
@role_required('user')
def get_latest_activity_user():
    return PredictController.get_latest_activity_user()
