from werkzeug.security import check_password_hash

def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    if isinstance(stored_password, bytes):
        stored_password = stored_password.decode('utf-8')
    return check_password_hash(stored_password, provided_password)
