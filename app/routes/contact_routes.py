from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import db, ContactForm

bp = Blueprint('contact_routes', __name__)

@bp.route('/contact', methods=['GET', 'POST'])
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

        return redirect(url_for('contact_routes.contact'))

    return render_template('contact.html')
