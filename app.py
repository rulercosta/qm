import os
from flask import Flask, render_template, send_file, session, request, flash, redirect, url_for
from models import db, Participant, Instructor, ContactForm
from database import init_db
from flask_session import Session
from dotenv import load_dotenv
import cert_gen
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

load_dotenv()

app = Flask(__name__)

# Database configuration (SQLite or PostgreSQL, depending on your preference)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Flask-Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')  # Directory for session files
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.secret_key = os.getenv('SESSION_SECRET_KEY')

# Initialize Flask-Session
Session(app)

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

def format_date_with_ordinal(date):
    day = date.day
    month = date.strftime('%B')
    year = date.strftime('%Y')

    # Determine the ordinal suffix
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    
    return f"{day}{suffix} {month}, {year}"

# Route to verify the certificate by its ID
@app.route('/programmes/workshops/verify/<cid>')
def verify_certificate(cid):
    participant = Participant.query.filter_by(cid=cid).first()
    if participant:
        instructor = Instructor.query.filter_by(courseid=participant.courseid).first()

        # Store participant and cid in session
        session['participant'] = {
            'name': participant.name,
            'workshop': instructor.course,
            'instructor': instructor.name,
            'date': format_date_with_ordinal(participant.date)
        }
        session['cid'] = cid  # Store Certificate ID in session

        return render_template(
            'verify.html',
            cid=cid,
            name=participant.name,
            instructor=instructor.name,
            profile=instructor.profile,
            course=instructor.course,
            date=format_date_with_ordinal(participant.date)
        )
    else:
        return render_template('verify.html', error="No record found")
    
@app.route('/programmes/workshops/verify/<cid>/download', methods=['POST'])
def download_certificate(cid):
    # Retrieve participant data from session
    participant_data = session.get('participant')
    
    if not participant_data:
        return "Session expired or invalid. Please verify the certificate again.", 400
    
    qr_data = f"https://quantummindsclub.onrender.com/programmes/workshops/verify/{cid}"
    
    # Use session data to generate the certificate
    certificate_image = cert_gen.generate_certificate_image(
        participant_data['name'],
        qr_data,
        "static/images/certificate_template.png",
        participant_data['workshop'],
        participant_data['instructor'],
        participant_data['date']
    )
    pdf_buffer = cert_gen.generate_certificate_pdf(certificate_image)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"{participant_data['name']}_certificate.pdf",
        mimetype='application/pdf'
    )

@app.route('/programmes/workshops')
def workshops():
    return render_template('error.html')

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        referral = request.form.get('referral')
        message_content = request.form.get('message')

        if not (name and email and phone and referral and message_content):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('contact'))

        # Save to database
        try:
            submission = ContactForm(
                name=name,
                email=email,
                phone=phone,
                referral=referral,
                message=message_content
            )
            db.session.add(submission)
            db.session.commit()
            flash('Your message has been received successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving your message. Please try again later.', 'error')
            print(f"Error: {e}")

        return redirect(url_for('contact'))

    return render_template('contact.html')

admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap4')
admin.add_view(ModelView(ContactForm, db.session))
admin.add_view(ModelView(Instructor, db.session))
admin.add_view(ModelView(Participant, db.session))

if __name__ == '__main__':
    app.run(debug=True)
