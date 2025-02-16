from flask import render_template, redirect, url_for
from . import home_bp as bp

@bp.route('/')
def root():
    return redirect(url_for('home.home'))

@bp.route('/home')
def home():
    return render_template('pages/home.jinja')

@bp.route('/about')
def about():
    return render_template('pages/about.jinja')
