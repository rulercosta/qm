from flask import Blueprint, render_template, session, send_file
from app.models import Participant, Instructor
from app.cert_gen import generate_certificate_image, generate_certificate_pdf
from app.utils import format_date_with_ordinal

bp = Blueprint('workshop_routes', __name__)

@bp.route('/programmes/workshops')
def workshops():
    # Logic to display workshops
    return render_template('error.html')

# Route to verify the certificate by its ID
@bp.route('/programmes/workshops/verify/<cid>')
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

@bp.route('/programmes/workshops/verify/<cid>/download', methods=['POST'])
def download_certificate(cid):
    # Retrieve participant data from session
    participant_data = session.get('participant')

    if not participant_data:
        return "Session expired or invalid. Please verify the certificate again.", 400

    qr_data = f"https://quantummindsclub.onrender.com/programmes/workshops/verify/{cid}"

    # Use session data to generate the certificate
    certificate_image = generate_certificate_image(
        participant_data['name'],
        qr_data,
        "static/images/certificate_template.png",
        participant_data['workshop'],
        participant_data['instructor'],
        participant_data['date']
    )
    pdf_buffer = generate_certificate_pdf(certificate_image)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"{participant_data['name']}_certificate.pdf",
        mimetype='application/pdf'
    )
