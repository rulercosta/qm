from flask import Flask
from app.configs.config import get_config
from app.utils.env_loader import load_environment
from app.utils.app_init import (
    init_extensions,
    register_blueprints,
    init_database,
    init_request_logging
)
from app.utils.logger import setup_loggers
from app.utils.paths import paths

def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = load_environment()
    
    app = Flask(__name__,
                template_folder=str(paths.templates_path),
                static_folder=str(paths.static_path))
    
    try:
        # Initialize logging first for better error tracking
        setup_loggers(app)
        app.logger.info("=== Starting Application Initialization ===")
        
        # Load configuration
        config_obj = get_config(config_name)
        app.config.from_object(config_obj)
        app.logger.info("Configuration loaded successfully")
        
        # Initialize components
        init_request_logging(app)
        app.logger.info("Request logging initialized")
        
        init_extensions(app)
        app.logger.info("Extensions initialized")
        
        init_database(app)
        app.logger.info("Database initialized")
        
        register_blueprints(app)
        app.logger.info("Blueprints registered")
        
        app.logger.info("=== Application Initialization Complete ===")
        return app
        
    except Exception as e:
        # Ensure we log any initialization errors
        if hasattr(app, 'logger'):
            app.logger.critical(f"Failed to initialize application: {str(e)}", exc_info=True)
        raise

