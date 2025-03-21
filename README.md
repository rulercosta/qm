# Quantum Minds

A technology innovation hub for the United College of Engineering and Research (UCER) student community, focusing on space tech, defense, AI, cybersecurity, and interdisciplinary research.

## About Quantum Minds

We are a student-driven innovation community that:
- Fosters interdisciplinary collaboration in cutting-edge technology
- Develops solutions for real-world challenges
- Supports hands-on projects and research initiatives
- Connects students across diverse engineering disciplines

## Key Focus Areas
- Space Technology
- Defense Technology
- Artificial Intelligence
- Cybersecurity
- Agricultural Engineering
- Bio-Medical Engineering
- Robotics
- Drone Technology

## Documentation

- [Architecture Overview](docs/architecture.md)
- [Environment Configuration](docs/configuration.md)
- [Installation Guide](docs/installation.md)
- [Directory Structure](docs/structure.md)

## Database Migration Instructions

### Migrating to the New Schema

The application has been updated with a new normalized database schema. To migrate your existing Supabase database:

1. Make sure your `.env` file has the following Supabase connection variable:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   ```
   
   You can typically construct this from your Supabase dashboard connection settings.

2. Install required packages:
   ```
   pip install psycopg2-binary python-dotenv
   ```

3. Run the migration script:
   ```
   python migrations/migration_schema.py
   ```

   If the primary migration script fails, try the alternative script:
   ```
   python migrations/alternative_migration.py
   ```

The migration will:
1. Create new normalized tables (`participants`, `courses`, `instructors`, `enrollments`)
2. Migrate data from old tables to the new structure
3. Generate secure IDs for certificates that can be safely shared with end-users
4. Keep the old tables with a different name for backup purposes

After migration, the application will use the new schema automatically.

### Note on Certificate URLs

- Old URLs with `?cid=XXX` will continue to work but will redirect to new secure URLs
- New certificate URLs will use `?id=XXX` with the secure ID that doesn't expose internal certificate IDs

## Local Development & Testing

### Synchronizing Local SQLite Database from Supabase

After migrating your Supabase database to the new schema, you'll need to update your local SQLite database for testing.

1. Make sure your `.env` file has the following variables:
   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   SQLITE_DB_PATH=/home/rulercosta/Desktop/Projects/qm/db.sqlite3
   ```

2. Run the synchronization script:
   ```
   python scripts/sync_sqlite_from_supabase.py
   ```

This script will:
1. Connect to both your Supabase database and local SQLite database
2. Recreate the schema in SQLite to match the new normalized structure
3. Copy all relevant data from Supabase to SQLite
4. Create necessary indexes for performance

After synchronization, your local testing environment will match the production database structure and data.

## License

This project is licensed under the MIT License. See the [LICENSE.md](LICENSE.md) file for details.