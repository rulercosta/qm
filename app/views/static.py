from flask import send_from_directory, current_app
import os
from . import static_bp as bp

@bp.route('/service-worker.js')
def service_worker():
    return send_from_directory(
        os.path.join(current_app.root_path, '..', 'static', 'js'),
        'service-worker.js',
        mimetype='application/javascript'
    )
