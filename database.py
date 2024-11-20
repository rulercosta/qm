import os
import csv
from datetime import datetime
from models import db, Participant, Instructor

def init_db(app):
    """Initialize the database and create tables if they don't exist."""
    with app.app_context():
        db.create_all()

        # Populate the database if it's empty
        if not Participant.query.first() and not Instructor.query.first():
            populate_database()

def populate_database():
    """Populate the database from CSV files."""
    # Load instructors.csv
    with open('instructors.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            instructor = Instructor(
                courseid=row['COURSEID'],
                course=row['COURSE'],
                name=row['NAME'],
                profile=row['PROFILE']
            )
            db.session.add(instructor)

    # Load participants.csv
    with open('participants.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            participant = Participant(
                cid=row['CID'],
                courseid=row['COURSEID'],
                date=datetime.strptime(row['DATE'], '%Y-%m-%d').date(),
                sid=row['SID'],
                name=row['NAME']
            )
            db.session.add(participant)

    db.session.commit()
