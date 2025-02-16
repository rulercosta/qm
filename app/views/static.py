from flask import Blueprint, send_from_directory, current_app
import os

bp = Blueprint('static', __name__)

@bp.route('/service-worker.js')
def service_worker():
    return send_from_directory(
        os.path.join(current_app.root_path, '..', 'static', 'js'),
        'service-worker.js',
        mimetype='application/javascript'
    )
