from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('home_routes', __name__)

@bp.route('/')
def root():
    return redirect(url_for('home_routes.home'))

@bp.route('/home')
def home():
    return render_template('home.jinja')

@bp.route('/about')
def about():
    return render_template('about.jinja')
