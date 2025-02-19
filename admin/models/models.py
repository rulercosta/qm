from flask_login import UserMixin
from app.utils.security import login_manager
from admin.utils.gen_hash import hash_pass
from app.extensions.extensions import db  
import json


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(256))  

    location = db.Column(db.String(100))
    linkedin_url = db.Column(db.String(200))
    twitter_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    avatar_url = db.Column(db.String(500))
    skills = db.Column(db.Text, default='[]')
    education = db.Column(db.Text, default='[]')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    def get_skills(self):
        return json.loads(self.skills) if self.skills else []
    
    def set_skills(self, skills_list):
        self.skills = json.dumps(skills_list)
        
    def get_education(self):
        if not self.education or self.education == '[]':
            return None
        return json.loads(self.education)
    
    def set_education(self, education_data):
        self.education = json.dumps(education_data)

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
