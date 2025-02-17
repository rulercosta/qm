from flask import render_template, request, flash, redirect, url_for, current_app, after_this_request
from app.models.models import db, ContactForm
from . import contact_bp as bp
import uuid

def mask_email(email):
    """Mask email address for logging"""
    if '@' in email:
        username, domain = email.split('@')
        return f"{username[:2]}***@{domain}"
    return "invalid_email"

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    request_id = str(uuid.uuid4())[:8]  # Generate short unique ID
    current_app.logger.info(f"[{request_id}] Contact form accessed with method: {request.method}")
    
    if request.method == 'POST':
        @after_this_request
        def add_header(response):
            if response.status_code == 302:  
                response.headers['Cache-Control'] = 'no-store'
            return response

        current_app.logger.info(f"[{request_id}] Processing form submission from {request.remote_addr}")
        
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        referral = request.form.get('referral')
        message_content = request.form.get('message')

        if not (name and email and phone and referral and message_content):
            current_app.logger.warning(f"[{request_id}] Invalid form submission - missing fields: " + 
                                     ', '.join(f for f in ['name', 'email', 'phone', 'referral', 'message'] 
                                             if not request.form.get(f)))
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('contact.contact'))

        try:
            current_app.logger.info(f"[{request_id}] Attempting database submission for {mask_email(email)}")
            submission = ContactForm(
                name=name,
                email=email,
                phone=phone,
                referral=referral,
                message=message_content
            )
            db.session.add(submission)
            db.session.commit()
            current_app.logger.info(f"[{request_id}] Successfully saved contact form for {mask_email(email)}")
            flash('Your message has been received successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"[{request_id}] Database error for {mask_email(email)}: {str(e)}", exc_info=True)
            flash('An error occurred while saving your message. Please try again later.', 'error')

        return redirect(url_for('contact.contact'))

    return render_template('pages/contact.jinja')
