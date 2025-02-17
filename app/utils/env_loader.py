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
    
    if not os.path.exists(dotenv_path):
        error_msg = f"No .env file found at {dotenv_path}"
        logger.critical(error_msg)
        raise FileNotFoundError(error_msg)
    
    load_dotenv(dotenv_path, override=True)
    logger.info(f"Loaded environment from {dotenv_path}")
    
    required_vars = ['FLASK_ENV', 'SESSION_SECRET_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
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
