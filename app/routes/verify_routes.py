from flask import Blueprint, render_template, session, send_file, url_for, request, current_app
from werkzeug.exceptions import InternalServerError
from app.models import Participant, Instructor
from app.helpers.certgen import generate_certificate_image
from app.helpers.utils import format_date_with_ordinal, resize_image
from app.helpers.db_utils import retry_on_error, session_scope
from io import BytesIO
import base64
import os
import os.path

bp = Blueprint('verify_routes', __name__)

@bp.route('/events/workshops/verify', methods=['GET'])
def verify_certificate():
    try:
        cid = request.args.get('cid')
        download = request.args.get('download')

        if not cid:
            return "Certificate ID (cid) is required.", 400

        session.pop('participant', None)
        session.pop('cid', None)

        # Query and store all necessary data within session scope
        with session_scope() as db_session:
            participant = db_session.query(Participant).filter_by(cid=cid).first()
            if not participant:
                return render_template('verify.jinja', error="No record found")
            
            instructor = db_session.query(Instructor).filter_by(courseid=participant.courseid).first()
            if not instructor:
                return render_template('verify.jinja', error="Instructor not found")

            # Store all needed data while in session
            participant_data = {
                'name': participant.name,
                'workshop': instructor.course,
                'instructor': instructor.name,
                'date': format_date_with_ordinal(participant.date)
            }
            instructor_data = {
                'name': instructor.name,
                'profile': instructor.profile,
                'course': instructor.course
            }

        session['participant'] = participant_data
        session['cid'] = cid

        qr_data = url_for('verify_routes.verify_certificate', cid=cid, _external=True)
        template_path = os.path.join(os.path.dirname(current_app.root_path), 'static', 'images', 'certificate_template.png')
        
        if not os.path.exists(template_path):
            current_app.logger.error(f"Template file missing at {template_path}")
            return render_template('verify.jinja', error="Certificate template is not configured")

        @retry_on_error()
        def generate_and_process_certificate():
            certificate_image = generate_certificate_image(
                participant_data['name'],
                qr_data,
                template_path,
                participant_data['workshop'],
                participant_data['instructor'],
                participant_data['date']
            )

            if download:
                img_buffer = BytesIO()
                try:
                    certificate_image.save(img_buffer, format="PNG")
                    img_buffer.seek(0)
                    return send_file(
                        img_buffer,
                        as_attachment=True,
                        download_name=f"{participant_data['name']}_certificate.png",
                        mimetype='image/png'
                    )
                finally:
                    img_buffer.close()

            try:
                thumbnail = resize_image(certificate_image, 600)
                buffer = BytesIO()
                thumbnail.save(buffer, format="PNG")
                base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
                return render_template(
                    'verify.jinja',
                    cid=cid,
                    name=participant_data['name'],
                    instructor=instructor_data['name'],
                    profile=instructor_data['profile'],
                    course=instructor_data['course'],
                    date=participant_data['date'],
                    certificate=base64_image
                )
            finally:
                buffer.close()
                certificate_image.close()
                thumbnail.close()

        return generate_and_process_certificate()

    except Exception as e:
        current_app.logger.error(f"Verification route error for CID {cid}: {str(e)}", exc_info=True)
        session.pop('participant', None)
        session.pop('cid', None)
        raise InternalServerError("An error occurred while processing your request. Please try again.")