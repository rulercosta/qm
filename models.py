from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

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

