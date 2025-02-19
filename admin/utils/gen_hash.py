from werkzeug.security import generate_password_hash

def hash_pass(password):
    """Hash a password for storing."""
    return generate_password_hash(password)
