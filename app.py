import os
from flask import Flask, render_template
from models import db, Participant
from database import initialize_database

app = Flask(__name__)

# Database configuration (SQLite or PostgreSQL, depending on your preference)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
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
        initialize_database(app, 'participants.csv')  # Import data from CSV if the database is empty
        is_initialized = True

from datetime import datetime

# Route to verify the certificate by its ID
@app.route('/workshops/verify/<cert_id>')
def verify_certificate(cert_id):
    participant = Participant.query.filter_by(cid=cert_id).first()
    if participant:
        # Convert date to desired format
        formatted_date = datetime.strptime(participant.date, "%Y-%m-%d").strftime("%d %B, %Y")

        # Add ordinal suffix to the day
        day = int(formatted_date.split()[0])
        suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        formatted_date = formatted_date.replace(str(day), f"{day}{suffix}")
        
        return render_template(
            'verify.html',
            name=participant.name,
            date=formatted_date,
            course=participant.course
        )
    else:
        return render_template('verify.html', error=f"No record found :(")

if __name__ == '__main__':
    app.run(debug=True)
