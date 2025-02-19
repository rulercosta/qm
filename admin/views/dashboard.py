from . import dashboard_bp as bp
from flask import render_template, request, make_response, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound

@bp.route('/')
@login_required
def root():
    return redirect(url_for('dashboard.index'))

@bp.route('/index')
@login_required
def index():
    return render_template('home/index.html', active='index')

@bp.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        active = get_active(request)
        
        if request.headers.get('HX-Request'):
            return render_template("home/" + template, active=active)
        
        return render_template("home/" + template, active=active)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except Exception:
        return render_template('home/page-500.html'), 500

@bp.route('/profile/view')
@login_required
def profile_view():
    response = make_response(render_template('includes/profile_content.html'))
    response.headers['Content-Type'] = 'text/html'
    return response

# Helper - Extract current page name from request
def get_active(request):
    try:
        active = request.path.split('/')[-1]
        if active == '':
            active = 'index'
        return active
    except Exception:
        return None
