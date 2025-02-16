from flask import render_template, redirect, url_for
from . import events_bp as bp


@bp.route('/events/workshops')
def workshops():
    return redirect(url_for('events.events'))

@bp.route('/events')
def events():
    return render_template('pages/events.jinja')