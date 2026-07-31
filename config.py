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

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "app",
        "static",
        "uploads"
    )

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    MAX_CONTENT_LENGTH = 500 * 1024 * 1024

    # PayPal
    PAYPAL_CLIENT_ID = os.environ.get(
        "PAYPAL_CLIENT_ID"
    )

    PAYPAL_CLIENT_SECRET = os.environ.get(
        "PAYPAL_CLIENT_SECRET"
    )