from flask import Flask, render_template
from models import db, Participant, Instructor
from database import init_db

app = Flask(__name__)

# Database configuration (SQLite or PostgreSQL, depending on your preference)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')v
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Flag to ensure initialization only happens once
is_initialized = False

@app.before_request
def setup_database():
    global is_initialized
    if not is_initialized:
        db.create_all()  # Create tables if they don't exist
        init_db(app)  # Initialize the database from CSV if the database is empty
        is_initialized = True

from datetime import datetime

# Route to verify the certificate by its ID
@app.route('/programmes/workshops/verify/<cid>')
def verify_certificate(cid):
    participant = Participant.query.filter_by(cid=cid).first()
    if participant:
        # Fetch the related instructor details using the courseid
        instructor = Instructor.query.filter_by(courseid=participant.courseid).first()

        return render_template(
            'verify.html',
            name=participant.name,
            instructor=instructor.name,
            profile=instructor.profile,
            course=instructor.course,
            date=participant.date.strftime('%d %B, %Y') 
        )
    else:
        return render_template('verify.html', error=f"No record found")

@app.route('/programmes/workshops/verify')
def verify():
    return render_template('error.html')

@app.route('/programmes/workshops')
def workshops():
    return render_template('error.html')

@app.route('/programmes/events')
def events():
    return render_template('error.html')

@app.route('/programmes')
def programmes():
    return render_template('error.html')

@app.route('/home')
def home():
    return render_template('error.html')

@app.route('/about')
def about():
    return render_template('error.html')

@app.route('/faqs')
def faqs():
    return render_template('error.html')

@app.route('/contact')
def contact():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
