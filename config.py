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

    print("DATABASE:", SQLALCHEMY_DATABASE_URI)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "app/static/uploads"

    MAX_CONTENT_LENGTH = 500 * 1024 * 1024


    # PayPal Sandbox

    PAYPAL_CLIENT_ID = os.environ.get(
        "PAYPAL_CLIENT_ID"
    )

    PAYPAL_CLIENT_SECRET = os.environ.get(
        "PAYPAL_CLIENT_SECRET"
    )

