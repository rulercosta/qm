from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define the Participant model
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sid = db.Column(db.String(15), nullable=False)
    cid = db.Column(db.String(100), unique=True, nullable=False)
    courseid = db.Column(db.String(15), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Participant {self.name}>"
