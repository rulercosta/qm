from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('events', __name__)

@bp.route('/events/workshops')
def workshops():
    return redirect(url_for('events.events'))

@bp.route('/events')
def events():
    return render_template('events.jinja')