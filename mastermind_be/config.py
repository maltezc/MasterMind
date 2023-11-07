import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Typical config setup"""

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Config for dev"""

    DEBUG = True