from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('events_routes', __name__)

@bp.route('/events/workshops')
def workshops():
    return redirect(url_for('events_routes.events'))

@bp.route('/events')
def events():
    # Logic to display workshops
    return render_template('events.jinja')