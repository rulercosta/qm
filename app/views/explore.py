from flask import render_template
from . import explore_bp as bp

@bp.route('/explore')
def explore():
    return render_template('pages/explore.jinja')
