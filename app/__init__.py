from dotenv import load_dotenv

load_dotenv()

import os

from flask import Flask

from config import Config
from .extensions import db
from .extensions import migrate
from .extensions import login_manager

from .main.routes import main


def create_app():

    app = Flask(
        __name__,
        instance_path="/tmp/instance"
    )

    os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    login_manager.init_app(app)

    from .auth.routes import auth
    from .booking.routes import booking
    from .admin.routes import admin
    from .store.routes import store
    from .student.routes import student
    from .payments.routes import payments

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(booking)
    app.register_blueprint(admin)
    app.register_blueprint(store)
    app.register_blueprint(student)
    app.register_blueprint(payments)

    with app.app_context():
        db.create_all()

    return app