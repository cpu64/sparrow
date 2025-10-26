# models/db.py
import psycopg2
import os
import sys


db_params = {
    'dbname': os.getenv('PGDATABASE', 'sparrow'),
    'user': os.getenv('PGUSER', 'sparrow'),
    'password': os.getenv('PGPASSWORD', 'overwriteme'),
    'host': os.getenv('PGHOST', 'localhost'),
    'port': os.getenv('PGPORT', 5432)
}

def get_db_connection():
    return psycopg2.connect(**db_params)

def init_db():
    conn = None
    cur = None
    try:
        from .users.avatar import AVATAR_COLUMN_LENGTHS

        conn = get_db_connection()
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("""
        CREATE SCHEMA IF NOT EXISTS sparrow;
        SET search_path TO sparrow;
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS avatars (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(%(name_length)s) NOT NULL,
            url TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
        );
        """, {'name_length': AVATAR_COLUMN_LENGTHS['name'][1]})

        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
        if conn:
            conn.close()
        sys.exit(1)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
