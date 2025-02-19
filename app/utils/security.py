import cloudinary
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

login_manager = LoginManager()
csrf = CSRFProtect()

def init_security(app):
    """Initialize security components and Cloudinary"""
    # Initialize security
    csrf.init_app(app)
    
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    
    # Initialize Cloudinary
    if all([app.config['CLOUDINARY_CLOUD_NAME'],
           app.config['CLOUDINARY_API_KEY'],
           app.config['CLOUDINARY_API_SECRET']]):
        cloudinary.config(
            cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=app.config['CLOUDINARY_API_KEY'],
            api_secret=app.config['CLOUDINARY_API_SECRET']
        )
        app.logger.info("Cloudinary initialized successfully")
    else:
        app.logger.warning("Cloudinary configuration is incomplete")
    
    return login_manager
