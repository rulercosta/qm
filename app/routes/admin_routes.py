from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint, redirect, url_for, request
from flask_login import current_user
from app.models import ContactForm, Instructor, Participant
from app.extensions import db, admin

bp = Blueprint('admin_routes', __name__)

class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.path))

class BaseModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.path))

# Model views with simpler configuration
class ContactFormView(BaseModelView):
    can_create = False
    column_list = ['name', 'email', 'phone', 'referral', 'message', 'timestamp']
    column_searchable_list = ['email', 'name']
    column_filters = ['timestamp']
    column_default_sort = ('timestamp', True)
    page_size = 25
    column_labels = {
        'timestamp': 'Submitted At'
    }

class InstructorView(BaseModelView):
    column_list = ['courseid', 'course', 'name', 'profile']
    column_searchable_list = ['name', 'course']
    form_excluded_columns = ['participants']

class ParticipantView(BaseModelView):
    column_list = ['cid', 'name', 'sid', 'courseid', 'date']
    column_searchable_list = ['name', 'sid']
    column_filters = ['date']
    can_export = True

def init_admin_views():
    """Initialize admin views after app context is created"""
    admin.add_view(ContactFormView(
        ContactForm, 
        db.session,
        name='Inquiries',
        endpoint='inquiries',
        menu_icon_type='envelope'
    ))
    admin.add_view(InstructorView(
        Instructor, 
        db.session, 
        name='Instructors',
        endpoint='instructors',
        menu_icon_type='chalkboard-teacher'
    ))
    admin.add_view(ParticipantView(
        Participant, 
        db.session, 
        name='Participants',
        endpoint='participants',
        menu_icon_type='users'
    ))