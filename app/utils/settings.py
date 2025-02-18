import os
from pathlib import Path

class Settings:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        self.root_path = Path(__file__).parent.parent.parent.resolve()
        self.env = os.getenv('FLASK_ENV', 'development')
        self.debug = self.env == 'development'
        self.testing = self.env == 'testing'
        
        # Logging settings
        self.logging_enabled = os.getenv('LOGS', 'true').lower() == 'true'
        self.file_logging_enabled = os.getenv('FILE_LOGGING', 'true').lower() == 'true'
        
        # Default to DEBUG if logging is enabled and level isn't specified or invalid
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR'}
        log_level = os.getenv('LOG_LEVEL', '').upper()
        
        if self.logging_enabled:
            self.log_level = log_level if log_level in valid_levels else 'DEBUG'
        else:
            self.log_level = 'INFO'  # Only startup logs
            
        self.startup_logging = True
        
        # Database settings
        self.db_url = os.getenv('DATABASE_URL')
        self.db_pool_size = int(os.getenv('DB_POOL_SIZE', '100'))
        self.db_max_overflow = int(os.getenv('DB_MAX_OVERFLOW', '50'))
        self.db_pool_timeout = int(os.getenv('DB_POOL_TIMEOUT', '30'))
        self.db_pool_recycle = int(os.getenv('DB_POOL_RECYCLE', '1800'))
        
        if not self.db_url and not self.testing:
            if self.debug:
                self.db_url = f'sqlite:///{self.root_path}/db.sqlite3'
            else:
                raise ValueError("DATABASE_URL must be set in production")

    def log_config(self, logger):
        """Log critical startup information"""
        startup_messages = [
            "=== Application Startup ===",
            f"Environment: {self.env}",
            f"Debug Mode: {self.debug}",
            f"Database URL: {self.db_url}",
            f"Database Pool Size: {self.db_pool_size}",
            f"Database Max Overflow: {self.db_max_overflow}",
            f"Database Pool Timeout: {self.db_pool_timeout}s",
            f"Logging Enabled: {self.logging_enabled}",
            f"Log Level: {self.log_level}",
            "=== Configuration Complete ==="
        ]
        
        for message in startup_messages:
            logger.info(message)

settings = Settings()
