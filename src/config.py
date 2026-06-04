import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration.

    All sensitive values are loaded from environment variables.
    The application will not start if required secrets are missing.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIN_DATABASE_URL = os.environ.get('MAIN_DATABASE_URL') or os.environ.get('DATABASE_URL')
    DATABASE_URL = MAIN_DATABASE_URL

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False

    REDIS_URL = os.environ.get('REDIS_URL', '')
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')

    LICENSE_JWT_SECRET = os.environ.get('LICENSE_JWT_SECRET')

    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', '')

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', '1800'))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', '604800'))


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


_configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}


def get_config():
    """Return the config class matching FLASK_ENV (default: DevelopmentConfig)."""
    env = os.environ.get('FLASK_ENV', 'development')
    return _configs.get(env, DevelopmentConfig)
