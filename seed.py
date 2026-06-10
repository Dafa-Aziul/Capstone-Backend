from app import create_app
from app.extensions import db
from app.models.user_model import User
from werkzeug.security import generate_password_hash

app = create_app()

def seed_admin():
    with app.app_context():
        # Cek apakah admin dengan email ini sudah ada
        email_admin = "admin@test.com"
        existing_admin = User.query.filter_by(email=email_admin).first()
        
        if existing_admin:
            print(f"✅ Akun admin ({email_admin}) sudah ada di database.")
            return

        # Buat admin baru
        admin_user = User(
            nama="Admin Test",
            email=email_admin,
            password=generate_password_hash("admin123"), # Hashing password
            role="admin",
            is_active=True
        )

        db.session.add(admin_user)
        db.session.commit()
        
        print("🎉 Berhasil menambahkan akun Admin Test!")
        print(f"Email    : {email_admin}")
        print(f"Password : admin123")

if __name__ == "__main__":
    seed_admin()