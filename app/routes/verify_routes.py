from flask import Blueprint, render_template, session, send_file, url_for, request
from app.models import Participant, Instructor
from app.helpers.certgen import generate_certificate_image
from app.helpers.utils import format_date_with_ordinal, resize_image
from io import BytesIO
import base64

bp = Blueprint('verify_routes', __name__)

@bp.route('/events/workshops/verify', methods=['GET'])
def verify_certificate():
    cid = request.args.get('cid')  
    download = request.args.get('download')  

    if not cid:
        return "Certificate ID (cid) is required.", 400

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
    qr_data = url_for('verify_routes.verify_certificate', cid=cid, _external=True)

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

        if download:
            img_buffer = BytesIO()
            certificate_image.save(img_buffer, format="PNG")
            img_buffer.seek(0)

            return send_file(
                img_buffer,
                as_attachment=True,
                download_name=f"{participant_data['name']}_certificate.png",
                mimetype='image/png'
            )

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