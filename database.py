import csv
from models import db, Participant

# Function to load data from CSV into the database
def load_data_from_csv(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        participants = []
        for row in csv_reader:
            # Create a Participant object for each row
            participants.append(
                Participant(
                    participant_name=row['NAME'],
                    workshop_date=row['COKEY'][:8],  # Extract date from COKEY (YYYYMMDD)
                    workshop_code=row['COKEY'],
                    college_id=row['SID'],
                    certificate_id=row['CID']
                )
            )
        return participants

# Function to initialize the database and import data if empty
def initialize_database(app, csv_file):
    with app.app_context():
        if not Participant.query.first():  # Check if the database is empty
            participants = load_data_from_csv(csv_file)
            db.session.bulk_save_objects(participants)  # Bulk insert participants
            db.session.commit()
