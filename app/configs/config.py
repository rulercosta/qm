import os
import random
import string
from datetime import timedelta
from app.utils.settings import settings

def get_database_url(flask_env):
    """Centralized database URL configuration"""
    return settings.db_url

class BaseConfig:
    SECRET_KEY = os.getenv('SESSION_SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))   
    
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

    
    # Cloudinary config
    CLOUDINARY_CLOUD_NAME = settings.cloudinary_cloud_name
    CLOUDINARY_API_KEY = settings.cloudinary_api_key
    CLOUDINARY_API_SECRET = settings.cloudinary_api_secret

    # CSRF Settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.getenv('CSRF_SECRET_KEY', os.urandom(32))
    WTF_CSRF_TIME_LIMIT = 3600
    WTF_CSRF_SSL_STRICT = False  # Set to True in production
    WTF_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
    
    # Session Settings
    SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)

    # Logging configuration
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = 'INFO'
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    # Default limit for all routes unless decorated specifically
    RATELIMIT_DEFAULT = "100 per minute"
    # Separate limits for specific endpoints can be set using decorators:
    # @limiter.limit("5 per minute") - for sensitive endpoints
    # @limiter.limit("1000 per day") - for API endpoints
    # @limiter.exempt - for static resources
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_STRATEGY = "fixed-window"  # Options: fixed-window, moving-window
    RATELIMIT_HEADERS_ENABLED = True     # Adds rate limit headers to responses

    @classmethod
    def init_app(cls, flask_env):
        cls.SQLALCHEMY_DATABASE_URI = get_database_url(flask_env)
        return cls

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False
    TESTING = False
    
    # Enhanced security settings
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # CSRF enhanced protection
    WTF_CSRF_SSL_STRICT = True
    WTF_CSRF_TIME_LIMIT = 1800  # 30 minutes
    
    # More restrictive default rate limit for production
    RATELIMIT_DEFAULT = "60 per minute"  # Global default
    RATELIMIT_KEY_PREFIX = "production"  # Prefix for rate limiting keys
    
    # Production logging
    LOG_LEVEL = 'ERROR'

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
