import os
from urllib.parse import urlparse

from dotenv import load_dotenv


load_dotenv()


def is_railway_private_host(database_url):
    """Return True when the URL points to Railway private networking."""
    try:
        hostname = urlparse(database_url).hostname or ''
    except ValueError:
        return False

    return hostname.endswith('.railway.internal')


def get_database_url():
    """Return a SQLAlchemy-compatible database URL.

    Railway commonly provides PostgreSQL URLs through DATABASE_URL.
    This helper normalizes common Postgres URL variants so SQLAlchemy
    consistently uses the installed psycopg2 driver.
    """
    database_url = os.environ.get('DATABASE_URL')
    public_database_url = os.environ.get('DATABASE_PUBLIC_URL')
    local_database_url = os.environ.get('LOCAL_DATABASE_URL')
    running_on_railway = bool(
        os.environ.get('RAILWAY_ENVIRONMENT')
        or os.environ.get('RAILWAY_PROJECT_ID')
        or os.environ.get('RAILWAY_SERVICE_ID')
    )

    # Local development cannot resolve Railway's private hostname.
    # Prefer a public TCP proxy URL or an explicit local database URL instead.
    if database_url and is_railway_private_host(database_url) and not running_on_railway:
        database_url = public_database_url or local_database_url

    if database_url:
        if database_url.startswith('postgres://'):
            return database_url.replace('postgres://', 'postgresql+psycopg2://', 1)
        if database_url.startswith('postgresql://'):
            return database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        return database_url

    return 'sqlite:///croptracker.db'

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = get_database_url()

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = get_database_url()

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
