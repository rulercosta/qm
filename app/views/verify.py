from flask import render_template, session, send_file, url_for, request, current_app, redirect
from werkzeug.exceptions import InternalServerError
from app.models.models import Participant, Instructor, Enrollment, Course
from app.utils.certgen import CertificateGenerator
from app.utils.utils import format_date_with_ordinal, resize_image
from app.utils.db_utils import retry_on_error, session_scope
from app.utils.paths import paths
from io import BytesIO
import base64
from . import verify_bp as bp

@bp.route('/events/workshops/verify', methods=['GET'])
def verify_certificate():
    try:
        # Accept either CID (for backward compatibility) or secure_id (for new URLs)
        cid = request.args.get('cid')
        secure_id = request.args.get('id')
        download = request.args.get('download')

        if not cid and not secure_id:
            return "Certificate identification is required.", 400

        session.pop('participant', None)
        session.pop('certificate_id', None)

        # Query and store all necessary data within session scope
        with session_scope() as db_session:
            enrollment = None
            
            if secure_id:
                # Find enrollment by secure_id
                enrollment = db_session.query(Enrollment).filter_by(secure_id=secure_id).first()
            elif cid:
                # For backward compatibility - find by CID but redirect to secure_id URL
                enrollment = db_session.query(Enrollment).filter_by(cid=cid).first()
                if enrollment:
                    # Redirect to the secure_id URL
                    return redirect(url_for('verify.verify_certificate', 
                                           id=enrollment.secure_id, 
                                           download=download))
            
            if not enrollment:
                return render_template('pages/verify.jinja', error="No record found")
            
            # Get participant info
            participant = db_session.query(Participant).filter_by(sid=enrollment.participant_id).first()
            if not participant:
                return render_template('pages/verify.jinja', error="Participant not found")
            
            # Get course info
            course = db_session.query(Course).filter_by(courseid=enrollment.course_id).first()
            if not course:
                return render_template('pages/verify.jinja', error="Course not found")
            
            # Get instructor info
            instructor = db_session.query(Instructor).filter_by(id=course.instructor_id).first()
            if not instructor:
                return render_template('pages/verify.jinja', error="Instructor not found")

            # Store all needed data while in session
            participant_data = {
                'name': participant.name,
                'workshop': course.name,
                'instructor': instructor.name,
                'date': format_date_with_ordinal(enrollment.date)
            }
            instructor_data = {
                'name': instructor.name,
                'profile': instructor.profile,
                'course': course.name
            }

        session['participant'] = participant_data
        session['certificate_id'] = secure_id  # Store secure_id instead of cid

        # Use secure_id in QR code
        qr_data = url_for('verify.verify_certificate', id=secure_id, _external=True)
        
        # Update template path resolution
        try:
            template_path = paths.get_static_path('images', 'certificate_template.png')
        except FileNotFoundError:
            current_app.logger.error("Certificate template is not configured")
            return render_template('pages/verify.jinja', error="Certificate template is not configured")

        @retry_on_error()
        def generate_and_process_certificate():
            cert_gen = CertificateGenerator(current_app)
            certificate_image = cert_gen.generate_certificate(
                participant_data['name'],
                qr_data,
                participant_data['workshop'],
                participant_data['instructor'],
                participant_data['date'],
                template_path
            )

            try:
                if download:
                    img_buffer = BytesIO()
                    certificate_image.save(img_buffer, format="PNG")
                    img_buffer.seek(0)
                    # Create a copy of the buffer's contents
                    response = send_file(
                        img_buffer,
                        as_attachment=True,
                        download_name=f"{participant_data['name']}_certificate.png",
                        mimetype='image/png'
                    )
                    # Add cleanup callback
                    @response.call_on_close
                    def cleanup():
                        img_buffer.close()
                        certificate_image.close()
                    return response

                # Handle non-download case
                thumbnail = resize_image(certificate_image, 600)
                buffer = BytesIO()
                thumbnail.save(buffer, format="PNG")
                base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()
                thumbnail.close()
                certificate_image.close()
                
                return render_template(
                    'pages/verify.jinja',
                    certificate_id=secure_id,  # Use secure_id instead of cid
                    cid=None,  
                    name=participant_data['name'],
                    instructor=instructor_data['name'],
                    profile=instructor_data['profile'],
                    course=instructor_data['course'],
                    date=participant_data['date'],
                    certificate=base64_image
                )
            except Exception as e:
                if 'certificate_image' in locals():
                    certificate_image.close()
                raise e

        return generate_and_process_certificate()

    except Exception as e:
        current_app.logger.error(f"Verification route error: {str(e)}", exc_info=True)
        session.pop('participant', None)
        session.pop('certificate_id', None)
        raise InternalServerError("An error occurred while processing your request. Please try again.")