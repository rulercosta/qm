from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_admin import Admin

db = SQLAlchemy()
session = Session()
admin = Admin(name='Admin Dashboard', template_mode='bootstrap4')

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = "auth.login"  

@login_manager.user_loader
def load_user(user_id):
    from app.models import AdminUser
    return AdminUser.query.get(int(user_id))


from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()