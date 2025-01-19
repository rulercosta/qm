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

# Admin will be initialized in create_app
admin = Admin()

@login_manager.user_loader
def load_user(user_id):
    from app.models import AdminUser
    return AdminUser.query.get(int(user_id))