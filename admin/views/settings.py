# -*- encoding: utf-8 -*-

from flask import render_template, request, jsonify, make_response
from flask_login import login_required, current_user
from app.extensions.extensions import db
from admin.models.models import Users
from admin.utils.check_hash import verify_pass
from admin.utils.gen_hash import hash_pass
from . import settings_bp as bp
import json
import cloudinary
import cloudinary.uploader

@bp.route('/settings/view')
@login_required
def settings_view():
    response = make_response(render_template('includes/settings_content.html'))
    response.headers['Content-Type'] = 'text/html'
    return response

@bp.route('/update/username', methods=['POST'])
@login_required
def update_username():
    new_username = request.form.get('new_username')
    print(f"Received username update request: {new_username}")
    
    if not new_username:
        return jsonify({'success': False, 'message': 'Username cannot be empty'}), 400
        
    if Users.query.filter_by(username=new_username).first():
        return jsonify({'success': False, 'message': 'Username already taken'}), 400
        
    try:
        current_user.username = new_username
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Username updated successfully',
            'username': new_username,
            'refresh': True
        })
    except Exception as e:
        print(f"Error updating username: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/update/password', methods=['POST'])
@login_required
def update_password():
    print("Password update request received")
    print("Form data:", request.form)
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Validate all fields are present
    if not current_password:
        return jsonify({'success': False, 'message': 'Current password is required'}), 400
    if not new_password:
        return jsonify({'success': False, 'message': 'New password is required'}), 400
    if not confirm_password:
        return jsonify({'success': False, 'message': 'Confirm password is required'}), 400
        
    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'New passwords do not match'}), 400
    
    # Verify current password
    if not verify_pass(current_password, current_user.password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
        
    try:
        current_user.password = hash_pass(new_password)
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Password updated successfully',
            'refresh': True
        })
    except Exception as e:
        print(f"Error updating password: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error updating password'}), 500

@bp.route('/update_location', methods=['POST'])
@login_required
def update_location():
    new_location = request.form.get('new_location')
    if not new_location:
        return jsonify({'success': False, 'message': 'Location cannot be empty'})
    
    try:
        current_user.location = new_location
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Location updated successfully',
            'location': new_location,
            'refresh': True
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/update_social_urls', methods=['POST'])
@login_required
def update_social_urls():
    linkedin = request.form.get('linkedin_url')
    twitter = request.form.get('twitter_url')
    github = request.form.get('github_url')
    
    try:
        current_user.linkedin_url = linkedin
        current_user.twitter_url = twitter
        current_user.github_url = github
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Social URLs updated successfully',
            'urls': {
                'linkedin': linkedin,
                'twitter': twitter,
                'github': github
            },
            'refresh': True
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/update_skills', methods=['POST'])
@login_required
def update_skills():
    try:
        skills_json = request.form.get('skills')
        print(f"Received skills JSON: {skills_json}")
        
        if not skills_json:
            return jsonify({'success': False, 'message': 'No skills provided'}), 400

        skills_list = json.loads(skills_json)
        print(f"Parsed skills list: {skills_list}")
        
        if not isinstance(skills_list, list):
            return jsonify({'success': False, 'message': 'Invalid skills format'}), 400

        current_user.set_skills(skills_list)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Skills updated successfully',
            'skills': skills_list,
            'refresh': True,
            'close_modal': False
        })
    except Exception as e:
        print(f"Error updating skills: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/update_education', methods=['POST'])
@login_required
def update_education():
    try:
        degree = request.form.get('degree')
        institution = request.form.get('institution')
        graduation_year = request.form.get('graduation_year')
        
        if not all([degree, institution, graduation_year]):
            return jsonify({'success': False, 'message': 'All fields are required'}), 400

        education_data = {
            'degree': degree,
            'institution': institution,
            'graduation_year': graduation_year
        }

        current_user.set_education(education_data)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Education updated successfully',
            'education': education_data,
            'refresh': True
        })
    except Exception as e:
        print(f"Error updating education: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/update/email', methods=['POST'])
@login_required
def update_email():
    new_email = request.form.get('new_email')
    current_password = request.form.get('current_password')
    
    if not all([new_email, current_password]):
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
        
    if not verify_pass(current_password, current_user.password):
        return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
        
    if Users.query.filter_by(email=new_email).first():
        return jsonify({'success': False, 'message': 'Email already in use'}), 400
        
    try:
        current_user.email = new_email
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Email updated successfully',
            'email': new_email,
            'refresh': True
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/update/avatar', methods=['POST'])
@login_required
def update_avatar():
    try:
        if 'avatar' not in request.files:
            return jsonify({'success': False, 'message': 'No file uploaded'}), 400
            
        file = request.files['avatar']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'}), 400

        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not file.filename.lower().endswith(tuple(allowed_extensions)):
            return jsonify({'success': False, 'message': 'Invalid file type'}), 400
            
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            file,
            folder="avatars",
            public_id=f"avatar_{current_user.id}",
            overwrite=True,
            resource_type="auto"
        )
        
        # Update user's avatar_url
        current_user.avatar_url = upload_result['secure_url']
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Avatar updated successfully',
            'avatar_url': upload_result['secure_url']
        })
        
    except Exception as e:
        print(f"Error updating avatar: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
