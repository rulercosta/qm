import os
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from sqlalchemy import event
from sqlalchemy import exc

db = SQLAlchemy()
session = Session()

def init_db_events():
    """Initialize database event listeners"""
    @event.listens_for(db.engine, 'connect')
    def connect(dbapi_connection, connection_record):
        connection_record.info['pid'] = os.getpid()

    @event.listens_for(db.engine, 'checkout')
    def checkout(dbapi_connection, connection_record, connection_proxy):
        pid = os.getpid()
        if connection_record.info['pid'] != pid:
            connection_record.connection = None
            raise exc.DisconnectionError(
                "Connection record belongs to pid %s, "
                "attempting to check out in pid %s" %
                (connection_record.info['pid'], pid)
            )