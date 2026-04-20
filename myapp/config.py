import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("FLASK_JWT_SECRET_KEY")
    
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_COOKIE_CSRF_PROTECT = False

    STRIPE_PUBLIC_KEY = os.environ.get("FLASK_STRIPE_PUBLIC_KEY")
    STRIPE_SECRET_KEY = os.environ.get("FLASK_STRIPE_SECRET_KEY")

    FLASK_CLIENT_ID = os.environ.get("FLASK_CLIENT_ID")
    FLASK_CLIENT_SECRET = os.environ.get("FLASK_CLIENT_SECRET")