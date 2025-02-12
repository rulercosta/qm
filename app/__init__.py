import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.extensions import db, session, init_db_events
from app.config import config
from app.routes import (
    home_routes, verify_routes, contact_routes,
    events_routes, explore_routes, static_routes
)

def create_app(config_name='default'):
    app = Flask(__name__,
                template_folder=os.path.join(os.getcwd(), 'templates'),
                static_folder=os.path.join(os.getcwd(), 'static'))
    
    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    session.init_app(app)

    # Setup logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/qm.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('QM startup')

    with app.app_context():
        init_db_events()
        
        # Register blueprints
        app.register_blueprint(home_routes.bp)
        app.register_blueprint(events_routes.bp)
        app.register_blueprint(verify_routes.bp)
        app.register_blueprint(contact_routes.bp)
        app.register_blueprint(explore_routes.bp)
        app.register_blueprint(static_routes.bp)

    return app

