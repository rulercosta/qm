from flask import Blueprint
from app.utils.paths import paths

# Common blueprint configuration
blueprint_config = {
    'template_folder': str(paths.admin_templates_path),
    'static_folder': str(paths.admin_static_path),
    'static_url_path': '/static',
    'url_prefix': '/admin'
}

# Create blueprints with common config
auth_bp = Blueprint('auth', __name__, **blueprint_config)
dashboard_bp = Blueprint('dashboard', __name__, **blueprint_config)
settings_bp = Blueprint('settings', __name__, **blueprint_config)
gallery_bp = Blueprint('gallery', __name__, **blueprint_config)

__all__ = ['auth_bp', 'dashboard_bp', 'settings_bp', 'gallery_bp']