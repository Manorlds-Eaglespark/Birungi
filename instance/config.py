import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    """Parent configuration class."""
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    use_reloader = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
