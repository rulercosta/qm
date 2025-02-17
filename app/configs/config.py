import os
from app.utils.env_loader import get_project_root
from app.utils.settings import settings

def get_database_url(flask_env):
    """Centralized database URL configuration"""
    if flask_env == 'development':
        db_path = os.path.join(get_project_root(), 'db.sqlite3')
        return f'sqlite:///{db_path}'
    return os.getenv('DATABASE_URL')

class BaseConfig:
    SECRET_KEY = os.getenv('SESSION_SECRET_KEY', 'default-dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(settings.root_path, 'flask_session')
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Use settings for database configuration
    SQLALCHEMY_DATABASE_URI = settings.db_url
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': settings.db_pool_size,
        'max_overflow': settings.db_max_overflow,
        'pool_timeout': settings.db_pool_timeout,
        'pool_recycle': settings.db_pool_recycle,
        'pool_pre_ping': True
    }
    SQLALCHEMY_POOL_PRE_PING = True
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024 

    @classmethod
    def init_app(cls, flask_env):
        cls.SQLALCHEMY_DATABASE_URI = get_database_url(flask_env)
        return cls

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestingConfig(BaseConfig):
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(flask_env):
    """Get configuration based on environment"""
    config_class = config.get(flask_env, config['default'])
    return config_class.init_app(flask_env)
