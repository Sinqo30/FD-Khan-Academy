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

    # Fix older postgres:// URLs
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Vercel only allows writing to /tmp
    UPLOAD_FOLDER = "/tmp/uploads"

    MAX_CONTENT_LENGTH = 500 * 1024 * 1024

    PAYPAL_CLIENT_ID = os.environ.get(
        "PAYPAL_CLIENT_ID"
    )

    PAYPAL_CLIENT_SECRET = os.environ.get(
        "PAYPAL_CLIENT_SECRET"
    )