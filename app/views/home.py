from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('home', __name__)

@bp.route('/')
def root():
    return redirect(url_for('home.home'))

@bp.route('/home')
def home():
    return render_template('pages/home.jinja')

@bp.route('/about')
def about():
    return render_template('pages/about.jinja')
