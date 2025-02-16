from flask import Blueprint

# Define all blueprints
home_bp = Blueprint('home', __name__, url_prefix='')
events_bp = Blueprint('events', __name__, url_prefix='')
explore_bp = Blueprint('explore', __name__, url_prefix='')
contact_bp = Blueprint('contact', __name__, url_prefix='')
verify_bp = Blueprint('verify', __name__, url_prefix='')
static_bp = Blueprint('static', __name__, url_prefix='')

# Export all blueprints
__all__ = ['home_bp', 'events_bp', 'explore_bp', 'contact_bp', 'verify_bp', 'static_bp']