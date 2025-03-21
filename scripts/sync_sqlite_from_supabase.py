import os
import sqlite3
import psycopg2
from dotenv import load_dotenv
import sys
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

# Database URLs
DATABASE_URL = os.getenv('DATABASE_URL')
SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH', str(Path(__file__).parents[1] / 'instance' / 'db.sqlite3'))

def connect_to_pg():
    """Connect to PostgreSQL (Supabase)"""
    try:
        print('Connecting to PostgreSQL database...')
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f'Error connecting to PostgreSQL: {e}')
        sys.exit(1)

def connect_to_sqlite():
    """Connect to SQLite database"""
    try:
        print(f'Connecting to SQLite database at {SQLITE_DB_PATH}...')
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(SQLITE_DB_PATH), exist_ok=True)
        
        conn = sqlite3.connect(SQLITE_DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f'Error connecting to SQLite: {e}')
        sys.exit(1)

def table_exists(cur, table_name):
    """Check if a table exists in SQLite"""
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cur.fetchone() is not None

def recreate_schema(sqlite_cur):
    """Recreate the new schema in SQLite"""
    print("Creating tables in SQLite...")
    
    # Drop existing tables if they exist
    tables = ['enrollments', 'participants', 'courses', 'instructors']
    for table in tables:
        sqlite_cur.execute(f"DROP TABLE IF EXISTS {table}")
    
    # Create tables in the correct order for foreign key constraints
    
    # Instructors table
    sqlite_cur.execute("""
        CREATE TABLE instructors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            profile TEXT NOT NULL
        )
    """)
    
    # Courses table
    sqlite_cur.execute("""
        CREATE TABLE courses (
            courseid TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            instructor_id INTEGER NOT NULL,
            FOREIGN KEY (instructor_id) REFERENCES instructors (id)
        )
    """)
    
    # Participants table
    sqlite_cur.execute("""
        CREATE TABLE participants (
            sid TEXT PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    # Enrollments table
    sqlite_cur.execute("""
        CREATE TABLE enrollments (
            id INTEGER PRIMARY KEY,
            cid TEXT UNIQUE,
            secure_id TEXT UNIQUE,
            participant_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            date DATE NOT NULL,
            FOREIGN KEY (participant_id) REFERENCES participants (sid),
            FOREIGN KEY (course_id) REFERENCES courses (courseid)
        )
    """)
    
    # Create index on secure_id
    sqlite_cur.execute("CREATE INDEX idx_enrollments_secure_id ON enrollments(secure_id)")
    
    print("Schema created successfully in SQLite")

def copy_data(pg_cur, sqlite_cur, sqlite_conn):
    """Copy data from PostgreSQL to SQLite"""
    
    # Copy instructors
    print("Copying instructors data...")
    pg_cur.execute("SELECT id, name, profile FROM instructors")
    instructors = pg_cur.fetchall()
    
    for instructor in instructors:
        id, name, profile = instructor
        sqlite_cur.execute(
            "INSERT INTO instructors (id, name, profile) VALUES (?, ?, ?)",
            (id, name, profile)
        )
    print(f"✓ {len(instructors)} instructors copied")
    
    # Copy courses
    print("Copying courses data...")
    pg_cur.execute("SELECT courseid, name, instructor_id FROM courses")
    courses = pg_cur.fetchall()
    
    for course in courses:
        courseid, name, instructor_id = course
        sqlite_cur.execute(
            "INSERT INTO courses (courseid, name, instructor_id) VALUES (?, ?, ?)",
            (courseid, name, instructor_id)
        )
    print(f"✓ {len(courses)} courses copied")
    
    # Copy participants
    print("Copying participants data...")
    pg_cur.execute("SELECT sid, name FROM participants")
    participants = pg_cur.fetchall()
    
    for participant in participants:
        sid, name = participant
        sqlite_cur.execute(
            "INSERT INTO participants (sid, name) VALUES (?, ?)",
            (sid, name)
        )
    print(f"✓ {len(participants)} participants copied")
    
    # Copy enrollments
    print("Copying enrollments data...")
    pg_cur.execute("SELECT id, cid, secure_id, participant_id, course_id, date FROM enrollments")
    enrollments = pg_cur.fetchall()
    
    for enrollment in enrollments:
        id, cid, secure_id, participant_id, course_id, date = enrollment
        
        # Convert PostgreSQL date to SQLite compatible format
        if isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d')
        
        sqlite_cur.execute(
            "INSERT INTO enrollments (id, cid, secure_id, participant_id, course_id, date) VALUES (?, ?, ?, ?, ?, ?)",
            (id, cid, secure_id, participant_id, course_id, date)
        )
    print(f"✓ {len(enrollments)} enrollments copied")
    
    # Commit changes
    sqlite_conn.commit()
    print("All data copied successfully to SQLite")

def sync_databases():
    """Main function to synchronize databases"""
    pg_conn = None
    sqlite_conn = None
    
    try:
        # Connect to both databases
        pg_conn, pg_cur = connect_to_pg()
        sqlite_conn, sqlite_cur = connect_to_sqlite()
        
        # Enable foreign keys in SQLite
        sqlite_cur.execute("PRAGMA foreign_keys = ON")
        
        # Recreate schema in SQLite
        recreate_schema(sqlite_cur)
        
        # Copy data from PostgreSQL to SQLite
        copy_data(pg_cur, sqlite_cur, sqlite_conn)
        
        print("\nDatabase synchronization completed successfully!")
        print(f"Your SQLite database at {SQLITE_DB_PATH} is now up-to-date with Supabase.")
        
    except Exception as e:
        print(f"Error during synchronization: {e}")
        import traceback
        traceback.print_exc()
        if sqlite_conn:
            sqlite_conn.rollback()
    finally:
        # Close connections
        if pg_conn:
            pg_conn.close()
        if sqlite_conn:
            sqlite_conn.close()
        print("Database connections closed")

if __name__ == "__main__":
    sync_databases()
