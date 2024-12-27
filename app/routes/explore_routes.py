from flask import Blueprint, render_template

bp = Blueprint('explore_routes', __name__)

@bp.route('/explore')
def explore():
    return render_template('explore.jinja')
