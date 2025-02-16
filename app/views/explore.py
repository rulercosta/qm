from flask import Blueprint, render_template

bp = Blueprint('explore', __name__)

@bp.route('/explore')
def explore():
    return render_template('pages/explore.jinja')
