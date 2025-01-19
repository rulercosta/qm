from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_admin import Admin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
session = Session()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  
bcrypt = Bcrypt()

# Simplify admin configuration
admin = Admin(
    name='QM Admin',
    template_mode='bootstrap3'
)

@login_manager.user_loader
def load_user(user_id):
    from app.models import AdminUser
    return AdminUser.query.get(int(user_id))