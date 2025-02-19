"""
Database Models
"""

from app.models.models import Participant, Instructor, ContactForm

# Registry of all models for database initialization
ALL_MODELS = [
    Participant,
    Instructor,
    ContactForm
]

def register_models(models_list):
    """Register additional models with the global registry"""
    ALL_MODELS.extend(models_list)