import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

def get_project_root():
    """Get the absolute path to the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_environment():
    """Load and validate environment variables"""
    project_root = get_project_root()
    dotenv_path = os.path.join(project_root, '.env')
    
    # Try to load .env file if it exists, but don't fail if it doesn't
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path, override=True)
        logger.info(f"Loaded environment from {dotenv_path}")
    else:
        logger.info("No .env file found, using system environment variables")
    
    # Validate required environment variables
    required_vars = ['FLASK_ENV', 'SESSION_SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        # Set defaults for development if FLASK_ENV is missing
        if 'FLASK_ENV' in missing_vars and not os.getenv('FLASK_ENV'):
            logger.warning("FLASK_ENV not set, defaulting to 'development'")
            os.environ['FLASK_ENV'] = 'development'
            missing_vars.remove('FLASK_ENV')
            
        # If still have missing vars, raise error
        if missing_vars:
            error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
            logger.critical(error_msg)
            raise ValueError(error_msg)
    
    flask_env = os.getenv('FLASK_ENV')
    valid_envs = ['development', 'production', 'testing']
    
    if flask_env not in valid_envs:
        error_msg = f"Invalid FLASK_ENV value: {flask_env}. Must be one of: {', '.join(valid_envs)}"
        logger.critical(error_msg)
        raise ValueError(error_msg)
    
    logger.info(f"Environment validated successfully: FLASK_ENV={flask_env}")
    return flask_env
