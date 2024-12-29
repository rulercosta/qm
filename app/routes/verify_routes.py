from flask import Blueprint, render_template, session, send_file, url_for
from app.models import Participant, Instructor
from app.helpers.certgen import generate_certificate_image
from app.helpers.utils import format_date_with_ordinal, resize_image
from io import BytesIO
import base64

bp = Blueprint('workshop_routes', __name__)

@bp.route('/events/workshops/verify/<cid>')
def verify_certificate(cid):
    participant = Participant.query.filter_by(cid=cid).first()
    if not participant:
        return render_template('verify.jinja', error="No record found")

    instructor = Instructor.query.filter_by(courseid=participant.courseid).first()
    if not instructor:
        return render_template('verify.jinja', error="Instructor not found")

    session['participant'] = {
        'name': participant.name,
        'workshop': instructor.course,
        'instructor': instructor.name,
        'date': format_date_with_ordinal(participant.date)
    }
    session['cid'] = cid

    participant_data = session['participant']
    qr_data = url_for('workshop_routes.verify_certificate', cid=cid, _external=True)

    try:
        certificate_image = generate_certificate_image(
            participant_data['name'],
            qr_data,
            "static/images/certificate_template.png",
            participant_data['workshop'],
            participant_data['instructor'],
            participant_data['date']
        )

        session['participant']['certificate'] = certificate_image

        thumbnail = resize_image(certificate_image, 600)

        buffer = BytesIO()
        thumbnail.save(buffer, format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return render_template(
            'verify.jinja',
            cid=cid,
            name=participant.name,
            instructor=instructor.name,
            profile=instructor.profile,
            course=instructor.course,
            date=participant_data['date'],
            certificate=base64_image
        )

    except Exception as e:
        return f"Error generating certificate: {str(e)}", 500

@bp.route('/events/workshops/verify/<cid>/download', methods=['POST'])
def download_certificate(cid):
    participant_data = session.get('participant')
    if not participant_data:
        return "Session expired or invalid. Please try again.", 400

    certificate_image = participant_data.get('certificate')
    if not certificate_image:
        return "Certificate not found in session.", 400

    try:        
        img_buffer = BytesIO()
        certificate_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)

        return send_file(
            img_buffer,
            as_attachment=True,
            download_name=f"{participant_data['name']}_certificate.png",
            mimetype='image/png'
        )

    except Exception as e:
        return f"Error downloading certificate: {str(e)}", 500
