import os
from flask import Flask
from app.extensions import db, session, admin
from app.routes import home_routes, verify_routes, contact_routes, admin_routes, events_routes, explore_routes
from app.config import Config

from app.extensions import login_manager

from app.extensions import bcrypt

from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'), static_folder=os.path.join(os.getcwd(), 'static'))
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    session.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)


    # Register blueprints
    app.register_blueprint(home_routes.bp)
    app.register_blueprint(events_routes.bp)
    app.register_blueprint(verify_routes.bp)
    app.register_blueprint(contact_routes.bp)
    app.register_blueprint(explore_routes.bp)
    app.register_blueprint(admin_routes.bp)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

