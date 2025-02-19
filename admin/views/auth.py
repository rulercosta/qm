from flask import render_template, redirect, request, url_for, session, flash
from flask_login import current_user, login_user, logout_user
from app.utils.security import login_manager
from admin.utils.check_hash import verify_pass
from admin.configs.forms import LoginForm
from admin.models.models import Users
from . import auth_bp as bp

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
        
    login_form = LoginForm()
    
    if request.method == 'POST':
        if not login_form.validate():
            flash('Invalid form submission. Please check your input.', 'error')
            return render_template('accounts/login.html', form=login_form)

        username = login_form.username.data
        password = login_form.password.data

        user = Users.query.filter_by(username=username).first()

        if user and verify_pass(password, user.password):
            login_user(user)
            session.permanent = True
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))

        flash('Invalid username or password', 'error')
        return render_template('accounts/login.html', form=login_form)

    return render_template('accounts/login.html', form=login_form)

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    session.clear()
    return redirect(url_for('auth.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@bp.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@bp.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@bp.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
