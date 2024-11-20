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