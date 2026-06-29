from flask import Blueprint
from app.controllers.merek_controller import MerekController
from app.middlewares.auth_middleware import login_required, role_required

# Create blueprint
merek_bp = Blueprint('merek', __name__, url_prefix='/merek')

# List dan Create
@merek_bp.get('')
@login_required
def list_mereks():
    return MerekController.list_mereks()


# Detail, Update, Delete
@merek_bp.get('/<int:id_merek>')
def get_merek_detail(id_merek):
    return MerekController.get_merek_detail(id_merek)

@merek_bp.post('')
@login_required
@role_required('admin')
def create_merek():
    return MerekController.create_merek()

@merek_bp.put('/<int:id_merek>')
@login_required
@role_required('admin')
def update_merek(id_merek):
    return MerekController.update_merek(id_merek)

@merek_bp.delete('/<int:id_merek>')
@login_required
@role_required('admin')
def delete_merek(id_merek):
    return MerekController.delete_merek(id_merek)
