from . import gallery_bp as bp
from flask import render_template, request, jsonify, current_app
from flask_login import login_required
import cloudinary
import cloudinary.uploader
from cloudinary.search import Search

@bp.route('/gallery')
@login_required
def gallery():
    return render_template('home/gallery.html', active='gallery')

@bp.route('/gallery/upload', methods=['POST'])
@login_required
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'message': 'No file provided'}), 400

        cloudinary.config(
            cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=current_app.config['CLOUDINARY_API_KEY'],
            api_secret=current_app.config['CLOUDINARY_API_SECRET']
        )

        file = request.files['file']

        result = cloudinary.uploader.upload(
            file,
            folder='gallery'
        )

        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'data': {
                'id': result['public_id'],
                'url': result['secure_url']
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/gallery/images', methods=['GET'])
@login_required
def get_images():
    try:
        cloudinary.config(
            cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=current_app.config['CLOUDINARY_API_KEY'],
            api_secret=current_app.config['CLOUDINARY_API_SECRET']
        )

        result = Search()\
            .expression('folder:gallery')\
            .execute()

        images = [{
            'id': item['public_id'],
            'img': item['secure_url']
        } for item in result['resources']]

        return jsonify({'success': True, 'images': images})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/gallery/delete', methods=['DELETE'])
@login_required
def delete_image():
    try:
        cloudinary.config(
            cloud_name=current_app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=current_app.config['CLOUDINARY_API_KEY'],
            api_secret=current_app.config['CLOUDINARY_API_SECRET']
        )

        image_id = request.json.get('id')
        
        result = cloudinary.uploader.destroy(image_id)
        
        if result.get('result') == 'ok':
            return jsonify({'success': True, 'message': 'Image deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete image'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
