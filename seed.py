from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

with app.app_context():

    admin = User.query.filter_by(
        email="admin@fdkhanacademy.com"
    ).first()

    if admin:
        print("Admin account already exists.")

    else:

        admin = User(
            first_name="FD",
            last_name="Admin",
            email="admin@fdkhanacademy.com",
            is_admin=True
        )

        admin.set_password("Admin123!")

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully!")