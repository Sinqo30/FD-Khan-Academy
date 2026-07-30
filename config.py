import os

class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "fd-khan-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///fdkhan.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "app/static/uploads"

    MAX_CONTENT_LENGTH = 500 * 1024 * 1024