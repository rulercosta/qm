import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

_FLASK_ENV = None

def get_project_root():
    """Get the absolute path to the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_env():
    """Get the current Flask environment"""
    global _FLASK_ENV
    if _FLASK_ENV is None:
        _FLASK_ENV = load_environment()
    return _FLASK_ENV

def load_environment():
    """Load and validate environment variables"""
    global _FLASK_ENV
    project_root = get_project_root()
    dotenv_path = os.path.join(project_root, '.env')
    
    # Determine if we're in a production environment
    is_production = bool(os.getenv('RENDER') or os.getenv('PRODUCTION'))
    
    # Try to load .env file if it exists
    using_env_file = False
    if os.path.exists(dotenv_path) and not is_production:
        load_dotenv(dotenv_path, override=True)
        using_env_file = True
        logger.info(f"Loaded environment from {dotenv_path}")
    else:
        logger.info("Using system environment variables")
    
    if is_production:
        logger.info("Running in production environment")
        # Force production settings
        os.environ['FLASK_ENV'] = 'production'
        os.environ['FLASK_DEBUG'] = '0'
        logger.info("Production mode enforced: debug disabled")
        
        if not os.getenv('DATABASE_URL'):
            logger.critical("DATABASE_URL not set in production environment")
            raise ValueError("DATABASE_URL must be set in production")
    
    # Validate required environment variables
    required_vars = ['FLASK_ENV', 'SESSION_SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        if 'FLASK_ENV' in missing_vars:
            default_env = 'development' if using_env_file else 'production'
            os.environ['FLASK_ENV'] = default_env
            logger.warning(f"FLASK_ENV not set, defaulting to: {default_env}")
            missing_vars.remove('FLASK_ENV')
        
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.critical(error_msg)
            raise ValueError(error_msg)
    
    # Validate FLASK_ENV
    flask_env = os.getenv('FLASK_ENV')
    valid_envs = ['development', 'production', 'testing']
    
    if flask_env not in valid_envs:
        flask_env = 'development' if using_env_file else 'production'
        os.environ['FLASK_ENV'] = flask_env
        logger.warning(f"Invalid FLASK_ENV value, defaulting to: {flask_env}")
    
    # Handle FLASK_DEBUG
    flask_debug = os.getenv('FLASK_DEBUG')
    if flask_debug is None:
        # Set default debug mode based on environment
        default_debug = '1' if (flask_env == 'development' and using_env_file) else '0'
        os.environ['FLASK_DEBUG'] = default_debug
        logger.info(f"FLASK_DEBUG not set, defaulting to: {default_debug}")
    else:
        # Validate debug value
        os.environ['FLASK_DEBUG'] = '1' if flask_debug.lower() in ('1', 'true') else '0'
    
    _FLASK_ENV = flask_env
    logger.info(f"Environment validated successfully: FLASK_ENV={flask_env}, FLASK_DEBUG={os.getenv('FLASK_DEBUG')}")
    return flask_env

def get_debug_mode():
    """Get the current Flask debug mode"""
    return os.getenv('FLASK_DEBUG', '').lower() in ('true', '1')
