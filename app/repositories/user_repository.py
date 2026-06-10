from app.extensions import db
from app.models.user_model import User


class UserRepository:
    
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(id_user):
        return User.query.get(id_user)

    @staticmethod
    def create(nama, email, password):
        user = User(nama=nama, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user