from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository


class AuthService:
    
    @staticmethod
    def register(nama, email, password):
        # 1. cek apakah user sudah ada
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            raise ValueError("Email sudah terdaftar")

        # 2. hash password dan crete user
        hashed_password = generate_password_hash(password)
        user = UserRepository.create(nama, email, hashed_password)
        return user

    @staticmethod
    def login(email, password):
        # 1. cek apakah user ada
        user = UserRepository.get_by_email(email)
        
        # 2. Mengecek apakah email ada dan verifikasi kecocokan hash password
        if not user or not check_password_hash(user.password, password):
            raise ValueError("Email atau password salah")
            
        # 3. Mengecek field is_active, tolak jika False
        if not user.is_active:
            raise ValueError("Akun tidak aktif. Silakan hubungi admin.")
            
        access_token = create_access_token(identity=str(user.id_user))
        return user, access_token