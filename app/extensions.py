from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_admin import Admin

db = SQLAlchemy()
session = Session()
admin = Admin(name='Admin Dashboard', template_mode='bootstrap4')
