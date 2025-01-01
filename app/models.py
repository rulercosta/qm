from flask_sqlalchemy import SQLAlchemy
from app.extensions import db

class Participant(db.Model):
    __tablename__ = 'participants'
    cid = db.Column(db.String, unique=True, primary_key=True)  # Certificate ID
    courseid = db.Column(db.String, db.ForeignKey('instructors.courseid'), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Workshop date
    sid = db.Column(db.String, nullable=False)  # Student ID
    name = db.Column(db.String, nullable=False)  # Student name

    # Relationship to link participants to their course
    course = db.relationship('Instructor', back_populates='participants')

    def __repr__(self):
        return f"<Participant {self.name}>"

class Instructor(db.Model):
    __tablename__ = 'instructors'
    courseid = db.Column(db.String, unique=True, primary_key=True)  # Course ID
    course = db.Column(db.String, nullable=False)  # Course name
    name = db.Column(db.String, nullable=False)  # Instructor name
    profile = db.Column(db.String, nullable=False)  # Profile image filename

    # Relationship to link instructors to their participants
    participants = db.relationship('Participant', back_populates='course')

    def __repr__(self):
        return f"<Instructor {self.name}>"

class ContactForm(db.Model):
    __tablename__ = 'formsubmissions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    referral = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.now())

    def __repr__(self):
        return f"<ContactFormSubmission {self.name} - {self.email}>"


from app.extensions import db, bcrypt
from flask_login import UserMixin

class AdminUser(db.Model, UserMixin):
    __tablename__ = "admin_user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hash the password using bcrypt and store it."""
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        """Verify the provided password against the stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    # Flask-Login methods
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        """Return the unique identifier of the user (must be a string)."""
        return str(self.id)
