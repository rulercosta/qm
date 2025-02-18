import os
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

db = SQLAlchemy()
session = Session()

def init_db_events():
    """Initialize database event listeners"""
    from sqlalchemy import event
    from sqlalchemy.engine import Engine

    @event.listens_for(Engine, "connect")
    def connect(dbapi_connection, connection_record):
        """Set pragmas on connect for SQLite"""
        if db.engine.url.drivername == 'sqlite':
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()