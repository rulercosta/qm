from flask import Blueprint, render_template, session, send_file
from app.models import Participant, Instructor
from app.helpers.cert_gen import generate_certificate_image, generate_certificate_pdf
from app.helpers.utils import format_date_with_ordinal

bp = Blueprint('workshop_routes', __name__)

@bp.route('/events/workshops/verify/<cid>')
def verify_certificate(cid):
    participant = Participant.query.filter_by(cid=cid).first()
    if participant:
        instructor = Instructor.query.filter_by(courseid=participant.courseid).first()

        session['participant'] = {
            'name': participant.name,
            'workshop': instructor.course,
            'instructor': instructor.name,
            'date': format_date_with_ordinal(participant.date)
        }
        session['cid'] = cid  

        return render_template(
            'verify.jinja',
            cid=cid,
            name=participant.name,
            instructor=instructor.name,
            profile=instructor.profile,
            course=instructor.course,
            date=format_date_with_ordinal(participant.date)
        )
    else:
        return render_template('verify.jinja', error="No record found")

@bp.route('/events/workshops/verify/<cid>/download', methods=['POST'])
def download_certificate(cid):
    participant_data = session.get('participant')

    if not participant_data:
        return "Session expired or invalid. Please verify the certificate again.", 400

    qr_data = f"https://quantummindsclub.onrender.com/events/workshops/verify/{cid}"

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
