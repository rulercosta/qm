from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import BaseForm
from wtforms import TextAreaField

class CustomAdmin(Admin):
    def add_view(self, view):
        """Override add_view to ensure proper template mode and static files"""
        view.template_mode = 'bootstrap4'
        return super().add_view(view)

    @property
    def base_template(self):
        """Ensure base template is always adminlte"""
        return 'admin/base.html'
