from app.extensions import db
from app.models.user_model import User
from sqlalchemy import or_


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
    
    @staticmethod
    def set_status_user(id_user): 
        user = User.query.get(id_user)

        if not user :
            raise ValueError(f"User tidak ditemukan")
        
        # Sederhanakan toggle boolean
        user.is_active = not user.is_active
            
        db.session.commit()
        return user

    @staticmethod
    def get_all(page=1, per_page=10, search=None): 
        query = User.query
        
        if search:
            query = query.filter(
                or_(User.nama.ilike(f"%{search}%"), User.email.ilike(f"%{search}%"))
            )
            
        query = query.order_by(User.nama)
        
        paginate = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return paginate.items, paginate.total, paginate.pages 

    