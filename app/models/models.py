from app.extensions.extensions import db

class Participant(db.Model):
    __tablename__ = 'participants'
    cid = db.Column(db.String, unique=True, primary_key=True)  
    courseid = db.Column(db.String, db.ForeignKey('instructors.courseid'), nullable=False)
    date = db.Column(db.Date, nullable=False)  
    sid = db.Column(db.String, nullable=False) 
    name = db.Column(db.String, nullable=False)  

    course = db.relationship('Instructor', back_populates='participants')

    def __repr__(self):
        return f"<Participant {self.name}>"

class Instructor(db.Model):
    __tablename__ = 'instructors'
    courseid = db.Column(db.String, unique=True, primary_key=True)  
    course = db.Column(db.String, nullable=False)  
    name = db.Column(db.String, nullable=False)  
    profile = db.Column(db.String, nullable=False)  

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
