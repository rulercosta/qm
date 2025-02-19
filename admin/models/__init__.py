"""
Database Models for admin authentication
"""

from admin.models.models import Users
from app.models import register_models

# List of admin models
ADMIN_MODELS = [
    Users
]

def init_admin_models():
    """Register admin models with the main app"""
    register_models(ADMIN_MODELS)