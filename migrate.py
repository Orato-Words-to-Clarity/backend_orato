import os
import psycopg2
from pathlib import Path

DATABASE_URL = os.getenv("DATABASE_URL")

SQL_FOLDER = "migrations/sql"
PYTHON_FOLDER = "migrations/pys"

def get_applied_migrations(cursor):
    """Fetch the list of applied migrations from the database."""
    cursor.execute("SELECT migration_name FROM migrations")
    return {row[0] for row in cursor.fetchall()}

def apply_sql_migration(cursor, file_name, file_path):
    """Apply a SQL migration."""
    print(f"Applying SQL migration: {file_name}")
    with open(file_path, "r") as file:
        sql = file.read()
        cursor.execute(sql)
    cursor.execute("INSERT INTO migrations (migration_name) VALUES (%s)", (file_name,))

def apply_python_migration(cursor, file_name, module_name):
    """Apply a Python migration by running its 'run' function."""
    print(f"Applying Python migration: {file_name}")
    migration_module = __import__(module_name, fromlist=["run"])
    migration_module.run(cursor)
    cursor.execute("INSERT INTO migrations (migration_name) VALUES (%s)", (file_name,))

def run_migrations():
    """Run all unapplied migrations except specific ones like 'latest.sql'."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()

    # Ensure the migrations table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id SERIAL PRIMARY KEY,
            migration_name TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Get already applied migrations
    applied_migrations = get_applied_migrations(cursor)

    # Apply SQL migrations, excluding 'latest.sql'
    sql_files = sorted(Path(SQL_FOLDER).glob("*.sql"))
    for file in sql_files:
        if file.name == "latest.sql":  # Skip 'latest.sql'
            continue
        if file.name not in applied_migrations:
            apply_sql_migration(cursor, file.name, file)

    # Apply Python migrations
    python_files = sorted(Path(PYTHON_FOLDER).glob("*.py"))
    for file in python_files:
        if file.name not in applied_migrations:
            module_name = f"migrations.pys.{file.stem}"
            apply_python_migration(cursor, file.name, module_name)

    cursor.close()
    conn.close()
    print("All migrations applied successfully!")

if __name__ == "__main__":
    run_migrations()
