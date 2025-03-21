import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import secrets
import datetime

# Load environment variables
load_dotenv()

# Use DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL')

def connect_to_db():
    """Connect to the PostgreSQL database server using DATABASE_URL"""
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cur = conn.cursor()
        return conn, cur
    except Exception as error:
        print(f'Error: {error}')
        raise

def execute_query(cur, query, fetch=False):
    """Execute a query and optionally fetch results"""
    try:
        print(f"Executing: {query[:60]}..." if len(query) > 60 else f"Executing: {query}")
        cur.execute(query)
        print("Query executed successfully")
        if fetch:
            return cur.fetchall()
        return None
    except Exception as e:
        print(f"Error executing query: {e}")
        raise

def table_exists(cur, table_name):
    """Check if a table exists in the database"""
    query = f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}')"
    cur.execute(query)
    return cur.fetchone()[0]

def run_migration():
    """Run database migration with more safeguards"""
    conn = None
    try:
        conn, cur = connect_to_db()
        
        # Check for existing tables
        if table_exists(cur, 'enrollments'):
            print("Migration already completed (enrollments table exists)")
            return
        
        # Grab participants data first
        if not table_exists(cur, 'participants'):
            print("ERROR: Participants table doesn't exist!")
            return
            
        # Get all participants first
        participant_data = execute_query(cur, "SELECT cid, sid, courseid, date, name FROM participants", fetch=True)
        if not participant_data:
            print("Warning: No participants found in database")
            return
            
        print(f"Found {len(participant_data)} participants to migrate")
        
        # Get instructor data
        instructor_data = execute_query(cur, "SELECT courseid, course, name, profile FROM instructors", fetch=True)
        if not instructor_data:
            print("Warning: No instructors found in database")
            return
            
        print(f"Found {len(instructor_data)} instructors to migrate")
        
        # Create backup tables
        print("Creating backup tables...")
        execute_query(cur, "CREATE TABLE participants_backup AS SELECT * FROM participants")
        execute_query(cur, "CREATE TABLE instructors_backup AS SELECT * FROM instructors")
        
        # Step 1: Create new normalized tables
        print("Creating new tables...")
        
        # Create instructors table (with id)
        execute_query(cur, """
            CREATE TABLE instructors_new (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                profile VARCHAR NOT NULL
            )
        """)
        
        # Create courses table
        execute_query(cur, """
            CREATE TABLE courses (
                courseid VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                instructor_id INTEGER REFERENCES instructors_new(id)
            )
        """)
        
        # Create participants table
        execute_query(cur, """
            CREATE TABLE participants_new (
                sid VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL
            )
        """)
        
        # Create enrollments table
        execute_query(cur, """
            CREATE TABLE enrollments (
                id SERIAL PRIMARY KEY,
                cid VARCHAR UNIQUE,
                secure_id VARCHAR(64) UNIQUE,
                participant_id VARCHAR REFERENCES participants_new(sid),
                course_id VARCHAR REFERENCES courses(courseid),
                date DATE NOT NULL
            )
        """)
        
        # Step 2: Migrate the data
        print("Migrating instructors...")
        
        # Keep track of unique instructors and their IDs
        instructor_map = {}
        
        # Insert instructors
        for record in instructor_data:
            courseid, course_name, instructor_name, profile = record
            if instructor_name not in instructor_map:
                # Add instructor if not already inserted
                execute_query(cur, f"""
                    INSERT INTO instructors_new (name, profile)
                    VALUES ('{instructor_name}', '{profile}')
                    RETURNING id
                """)
                instructor_id = cur.fetchone()[0]
                instructor_map[instructor_name] = instructor_id
            else:
                instructor_id = instructor_map[instructor_name]
                
            # Add course for this instructor
            execute_query(cur, f"""
                INSERT INTO courses (courseid, name, instructor_id)
                VALUES ('{courseid}', '{course_name}', {instructor_id})
            """)
            
        print("Migrating participants...")
        
        # Track unique participant IDs to avoid duplicates
        participant_ids = set()
        
        # Insert unique participants
        for record in participant_data:
            cid, sid, courseid, date, name = record
            if sid not in participant_ids:
                execute_query(cur, f"""
                    INSERT INTO participants_new (sid, name)
                    VALUES ('{sid}', '{name}')
                """)
                participant_ids.add(sid)
                
        print("Creating enrollments...")
        
        # Create enrollments
        for record in participant_data:
            cid, sid, courseid, date_value, name = record
            # Generate a secure ID
            secure_id = secrets.token_urlsafe(32)
            
            # Format date properly
            if isinstance(date_value, datetime.date):
                date_str = date_value.isoformat()
            else:
                # Handle string date format if needed
                date_str = date_value
                
            execute_query(cur, f"""
                INSERT INTO enrollments (cid, secure_id, participant_id, course_id, date)
                VALUES ('{cid}', '{secure_id}', '{sid}', '{courseid}', '{date_str}')
            """)
            
        # Create index on secure_id
        execute_query(cur, "CREATE INDEX idx_enrollments_secure_id ON enrollments(secure_id)")
        
        # Step 3: Swap the tables
        print("Swapping tables...")
        
        # Rename old tables
        execute_query(cur, "ALTER TABLE participants RENAME TO participants_old")
        execute_query(cur, "ALTER TABLE instructors RENAME TO instructors_old")
        
        # Rename new tables
        execute_query(cur, "ALTER TABLE participants_new RENAME TO participants")
        execute_query(cur, "ALTER TABLE instructors_new RENAME TO instructors")
        
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    run_migration()
