import os
from flask import request

def init_request_logging(app):
    """Setup request logging middleware"""
    @app.before_request
    def log_request_info():
        app.logger.info(f"Request: {request.method} {request.url}")

    @app.after_request
    def log_response_info(response):
        app.logger.info(f"Response: {response.status}")
        return response

def init_extensions(app):
    """Initialize Flask extensions"""
    from app.extensions.extensions import db, session, init_db_events
    
    db.init_app(app)
    session.init_app(app)
    
    with app.app_context():
        init_db_events()

def register_blueprints(app):
    """Register Flask blueprints"""
    from app.views import (
        home, verify, contact,
        events, explore, static
    )
    from admin.views import (
        auth, dashboard, gallery, settings
    )
    
    blueprints = [
        home.bp,
        events.bp,
        verify.bp,
        contact.bp,
        explore.bp,
        static.bp,
        auth.bp,
        dashboard.bp,
        gallery.bp,
        settings.bp
    ]
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

def init_database(app):
    """Initialize database based on configuration"""
    from app.extensions.extensions import db
    from admin.models import init_admin_models
    from app.utils.db_setup import create_admin_user
    
    # Register admin models before creating tables
    init_admin_models()
    
    with app.app_context():
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            db_exists = os.path.exists(db_path)
            
            # Create all registered models
            db.create_all()
            
            # Create admin user if INIT_ADMIN_USER is True
            if os.getenv('INIT_ADMIN_USER', 'True').lower() == 'true':
                if create_admin_user():
                    app.logger.info("Admin user created successfully")
            
            if not db_exists:
                app.logger.info(f"Initialized new SQLite database at {db_path}")
        else:
            db.create_all()
