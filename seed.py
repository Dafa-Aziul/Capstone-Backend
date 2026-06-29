from app import create_app
from app.extensions import db
from app.models.user_model import User
from werkzeug.security import generate_password_hash

app = create_app()


def seed_superadmin():
    with app.app_context():
        email_superadmin = "superadmin@test.com"
        existing_superadmin = User.query.filter_by(email=email_superadmin).first()

        if existing_superadmin:
            print(f"Akun superadmin ({email_superadmin}) sudah ada di database.")
            return

        superadmin_user = User(
            nama="Superadmin Test",
            email=email_superadmin,
            password=generate_password_hash("superadmin123"),
            role="superadmin",
            is_active=True,
        )

        db.session.add(superadmin_user)
        db.session.commit()

        print("Berhasil menambahkan akun Superadmin Test!")
        print(f"Email    : {email_superadmin}")
        print("Password : superadmin123")


if __name__ == "__main__":
    seed_superadmin()
