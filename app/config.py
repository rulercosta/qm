import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    SECRET_KEY = os.getenv('SESSION_SECRET_KEY', 'default-dev-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'flask_session')
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_POOL_SIZE', '5')),
        'pool_recycle': 1800,
        'pool_timeout': 30,
        'max_overflow': 10
    }
    SQLALCHEMY_POOL_PRE_PING = True
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024 
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 

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
