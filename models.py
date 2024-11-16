from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Participant model
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workshop_date = db.Column(db.String(50), nullable=False)
    workshop_code = db.Column(db.String(50), nullable=False)
    college_id = db.Column(db.String(50), nullable=False)
    certificate_id = db.Column(db.String(100), unique=True, nullable=False)
    participant_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Participant {self.participant_name}>"
