from app.extensions.extensions import db
import secrets

class Participant(db.Model):
    __tablename__ = 'participants'
    sid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    enrollments = db.relationship('Enrollment', back_populates='participant')
    
    def __repr__(self):
        return f"<Participant {self.name}>"

class Course(db.Model):
    __tablename__ = 'courses'
    courseid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))
    
    instructor = db.relationship('Instructor', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course')
    
    def __repr__(self):
        return f"<Course {self.name}>"

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.String, unique=True)  # Certificate ID
    secure_id = db.Column(db.String(64), unique=True, index=True)  # Public-facing ID
    participant_id = db.Column(db.String, db.ForeignKey('participants.sid'), nullable=False)
    course_id = db.Column(db.String, db.ForeignKey('courses.courseid'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    
    participant = db.relationship('Participant', back_populates='enrollments')
    course = db.relationship('Course', back_populates='enrollments')
    
    def __init__(self, **kwargs):
        # Generate a secure_id if not provided
        if 'secure_id' not in kwargs:
            kwargs['secure_id'] = secrets.token_urlsafe(32)
        super(Enrollment, self).__init__(**kwargs)
    
    def __repr__(self):
        return f"<Enrollment {self.cid}>"

class Instructor(db.Model):
    __tablename__ = 'instructors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    profile = db.Column(db.String, nullable=False)
    
    courses = db.relationship('Course', back_populates='instructor')
    
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
