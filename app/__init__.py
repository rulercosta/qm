import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.extensions.extensions import db, session, init_db_events
from app.configs.config import config
from app.views import (
    home, verify, contact,
    events, explore, static
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
        app.register_blueprint(home.bp)
        app.register_blueprint(events.bp)
        app.register_blueprint(verify.bp)
        app.register_blueprint(contact.bp)
        app.register_blueprint(explore.bp)
        app.register_blueprint(static.bp)

    return app

