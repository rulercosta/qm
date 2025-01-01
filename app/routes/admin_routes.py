from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint
from app.models import ContactForm, Instructor, Participant

bp = Blueprint('admin_routes', __name__)

from app.extensions import db
from app.extensions import admin


from flask_login import current_user
from flask import redirect, url_for

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


admin.add_view(AuthenticatedModelView(ContactForm, db.session))
admin.add_view(AuthenticatedModelView(Instructor, db.session))
admin.add_view(AuthenticatedModelView(Participant, db.session))