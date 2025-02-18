import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from flask import request, has_request_context
from .paths import paths
from .settings import settings

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.method = request.method
        else:
            record.url = "startup"
            record.remote_addr = "system"
            record.method = "INIT"
        return super().format(record)

def setup_loggers(app):
    """Configure application logging with multiple handlers"""
    app.logger.handlers.clear()
    
    # Basic format for all logs
    log_format = '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s'
    startup_format = '[%(asctime)s] %(levelname)s: %(message)s'
    
    # Always show startup logs (regardless of LOG_LEVEL)
    startup_handler = logging.StreamHandler()
    startup_handler.setFormatter(logging.Formatter(startup_format))
    startup_handler.setLevel(logging.INFO)
    app.logger.addHandler(startup_handler)
    app.logger.setLevel(logging.INFO)
    
    # Show startup information
    settings.log_config(app.logger)
    
    # Setup file handlers if enabled
    if settings.file_logging_enabled:
        app.logger.info("Configuring file-based log handlers...")
        
        log_handlers = []
        
        # Application handler
        app_handler = RotatingFileHandler(
            paths.logs_path / 'app.log',
            maxBytes=10 * 1024 * 1024,
            backupCount=10
        )
        app_handler.setFormatter(logging.Formatter(log_format))
        app_handler.setLevel(logging.INFO)
        log_handlers.append(app_handler)
        
        # Error handler
        error_handler = TimedRotatingFileHandler(
            paths.logs_path / 'error.log',
            when='midnight',
            interval=1,
            backupCount=30
        )
        error_handler.setFormatter(logging.Formatter(log_format))
        error_handler.setLevel(logging.ERROR)
        log_handlers.append(error_handler)
        
        # Add all handlers
        for handler in log_handlers:
            app.logger.addHandler(handler)
        
        app.logger.info("File handlers configured successfully")
        app.logger.info(f"Log files will be stored in: {paths.logs_path}")
    else:
        app.logger.info("File-based logging is disabled")
    
    if settings.logging_enabled:
        app.logger.info("Console logging is enabled")
    else:
        app.logger.info("Console logging is disabled (only startup logs will be shown)")
    
    app.logger.info("Logger initialization complete")
    
    # Switch to configured logging level after startup
    if settings.logging_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        console_handler.setLevel(getattr(logging, settings.log_level))
        app.logger.addHandler(console_handler)
        app.logger.info(f"Switching to {settings.log_level} logging level")
    
    # Remove startup handler after initialization
    app.logger.removeHandler(startup_handler)
    
    # Set final log level
    app.logger.setLevel(getattr(logging, settings.log_level))
    
    # Setup database logging
    if settings.file_logging_enabled:
        db_logger = logging.getLogger('sqlalchemy.engine')
        db_handler = RotatingFileHandler(
            paths.logs_path / 'db.log',
            maxBytes=10 * 1024 * 1024,
            backupCount=5
        )
        db_handler.setFormatter(logging.Formatter(log_format))
        db_logger.addHandler(db_handler)
        db_logger.setLevel(logging.WARNING)
