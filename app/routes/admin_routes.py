from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint
from app import db
from app.models import ContactForm, Instructor, Participant

bp = Blueprint('admin_routes', __name__)

from app.extensions import admin

admin.add_view(ModelView(ContactForm, db.session))
admin.add_view(ModelView(Instructor, db.session))
admin.add_view(ModelView(Participant, db.session))
