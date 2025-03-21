import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import secrets
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

# Use DATABASE_URL instead of individual connection parameters
DATABASE_URL = os.getenv('DATABASE_URL')

def connect_to_db():
    """Connect to the PostgreSQL database server using DATABASE_URL"""
    try:
        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        # Create a cursor
        cur = conn.cursor()
        
        # Print PostgreSQL version
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(f'PostgreSQL database version: {db_version}')
        
        return conn, cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'Error: {error}')
        raise

def execute_sql(cur, sql):
    """Execute an SQL command and print success"""
    try:
        print(f"Executing: {sql[:60]}...")
        cur.execute(sql)
        print("Command executed successfully")
    except Exception as e:
        print(f"Error executing SQL: {e}")
        raise

def migrate_database():
    """Migrate the database from old schema to new normalized schema"""
    conn = None
    try:
        # Connect to the database
        conn, cur = connect_to_db()
        
        # Check if we're connected to the correct database
        url_parts = urlparse(DATABASE_URL)
        db_name = url_parts.path.lstrip('/')
        print(f"Connected to database: {db_name}")
        
        # 1. First check if the tables exist
        print("Checking existing tables...")
        
        # Check if old participant table exists
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'participants')")
        participants_exists = cur.fetchone()[0]
        
        if not participants_exists:
            print("Error: Original 'participants' table not found. Cannot migrate data.")
            return
        
        # Check if enrollments table already exists
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'enrollments')")
        enrollments_exists = cur.fetchone()[0]
        
        if not enrollments_exists:
            # First, back up existing tables
            print("Backing up existing tables...")
            execute_sql(cur, "CREATE TABLE IF NOT EXISTS participants_old AS SELECT * FROM participants")
            execute_sql(cur, "CREATE TABLE IF NOT EXISTS instructors_old AS SELECT * FROM instructors")
            
            # Continue with migration as before...
            print("Creating new tables...")
            
            # Create participants table with new structure
            execute_sql(cur, """
                CREATE TABLE IF NOT EXISTS participants_new (
                    sid VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL
                )
            """)
            
            # Create instructors table with numeric id
            execute_sql(cur, """
                CREATE TABLE IF NOT EXISTS instructors_new (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    profile VARCHAR NOT NULL
                )
            """)
            
            # Create courses table
            execute_sql(cur, """
                CREATE TABLE IF NOT EXISTS courses (
                    courseid VARCHAR PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    instructor_id INTEGER REFERENCES instructors_new(id)
                )
            """)
            
            # Create enrollments table
            execute_sql(cur, """
                CREATE TABLE IF NOT EXISTS enrollments (
                    id SERIAL PRIMARY KEY,
                    cid VARCHAR UNIQUE,
                    secure_id VARCHAR(64) UNIQUE,
                    participant_id VARCHAR REFERENCES participants_new(sid),
                    course_id VARCHAR REFERENCES courses(courseid),
                    date DATE NOT NULL
                )
            """)
            
            # 2. Migrate data from old tables to new tables
            print("Migrating data from old tables to new tables...")
            
            # Migrate instructors data
            execute_sql(cur, """
                INSERT INTO instructors_new (name, profile)
                SELECT name, profile FROM instructors
            """)
            
            # Get instructor id mappings for later use
            cur.execute("""
                SELECT i.courseid, i_new.id 
                FROM instructors i
                JOIN instructors_new i_new ON i.name = i_new.name AND i.profile = i_new.profile
            """)
            instructor_mappings = {row[0]: row[1] for row in cur.fetchall()}
            
            # Migrate courses from instructors
            for old_courseid, instructor_id in instructor_mappings.items():
                execute_sql(cur, f"""
                    INSERT INTO courses (courseid, name, instructor_id)
                    SELECT courseid, course, {instructor_id} FROM instructors WHERE courseid = '{old_courseid}'
                """)
            
            # Extract unique participants
            execute_sql(cur, """
                INSERT INTO participants_new (sid, name)
                SELECT DISTINCT ON (sid) sid, name FROM participants
            """)
            
            # Migrate enrollments with secure_id - FIXED QUERY EXECUTION
            print("Migrating participants to enrollments...")
            cur.execute("SELECT cid, sid, courseid, date FROM participants")
            participants_data = cur.fetchall()
            
            if not participants_data:
                print("Warning: No participants found to migrate.")
            
            for participant in participants_data:
                cid, sid, courseid, date = participant
                secure_id = secrets.token_urlsafe(32)
                print(f"Adding enrollment for {sid} in course {courseid}")
                execute_sql(cur, f"""
                    INSERT INTO enrollments (cid, secure_id, participant_id, course_id, date)
                    VALUES ('{cid}', '{secure_id}', '{sid}', '{courseid}', '{date}')
                """)
            
            # 5. Add index on secure_id
            execute_sql(cur, """
                CREATE INDEX IF NOT EXISTS idx_enrollments_secure_id ON enrollments(secure_id)
            """)
            
            # 6. Rename and swap tables 
            execute_sql(cur, "ALTER TABLE participants RENAME TO participants_temp")
            execute_sql(cur, "ALTER TABLE participants_new RENAME TO participants")
            execute_sql(cur, "ALTER TABLE instructors RENAME TO instructors_temp") 
            execute_sql(cur, "ALTER TABLE instructors_new RENAME TO instructors")
            
            print("Migration completed successfully")
        else:
            print("New schema already exists. Skipping migration.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
        import traceback
        traceback.print_exc()  # Print full stack trace for easier debugging
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    migrate_database()
