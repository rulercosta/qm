from contextlib import contextmanager
from flask import current_app
from time import sleep
from functools import wraps

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    from app.extensions import db
    session = db.session
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def retry_on_error(retries=3, delay=0.5):
    """Decorator to retry functions on error with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt == retries - 1:
                        current_app.logger.error(f"Final retry attempt failed: {str(e)}")
                        raise
                    sleep(delay * (2 ** attempt))
                    current_app.logger.warning(f"Retrying operation, attempt {attempt + 1}")
            raise last_error
        return wrapper
    return decorator
