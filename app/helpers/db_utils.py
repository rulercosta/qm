from contextlib import contextmanager
from time import sleep
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Base class for database related errors"""
    pass

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    from app.extensions import db
    session = db.session
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Database error: {str(e)}", exc_info=True)
        raise DatabaseError(f"Database operation failed: {str(e)}")
    finally:
        session.close()

def retry_on_error(retries=3, delay=0.5, exceptions=(DatabaseError,)):
    """Enhanced retry decorator with specific exception handling"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if attempt == retries - 1:
                        logger.error(f"All retry attempts failed for {func.__name__}: {str(e)}")
                        raise
                    wait_time = delay * (2 ** attempt)
                    logger.warning(f"Retrying {func.__name__}, attempt {attempt + 1} after {wait_time}s")
                    sleep(wait_time)
            raise last_error
        return wrapper
    return decorator
