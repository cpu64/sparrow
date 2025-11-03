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

def execute(query, values=()):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        conn.commit()

    except Exception as e:
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_one(query, values=()):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        data = cur.fetchone()

        if data:
            columns = [desc[0] for desc in cur.description]
            data_dict = dict(zip(columns, data))
            return data_dict
        return None
    except Exception as e:
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_all(query, values=()):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        data = cur.fetchall()

        if data:
            columns = [desc[0] for desc in cur.description]
            data_dict = [dict(zip(columns, i)) for i in data]
            return data_dict
        return []

    except Exception as e:
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def init_db():
    conn = None
    cur = None
    try:
        from .users.avatar import AVATAR_COLUMN_LENGTHS
        from .users.user import USER_COLUMN_LENGTHS

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
            name VARCHAR(%(name_length)s) UNIQUE NOT NULL,
            url TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
        );
        """, {'name_length': AVATAR_COLUMN_LENGTHS['name'][1]})

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            username VARCHAR(%(username_length)s) UNIQUE NOT NULL,
            password VARCHAR(%(password_length)s) NOT NULL,
            twofa_secret VARCHAR(%(twofa_secret_length)s),
            name VARCHAR(%(name_length)s),
            surname VARCHAR(%(surname_length)s),
            email VARCHAR(%(email_length)s),
            description VARCHAR(%(description_length)s),
            date_of_birth TIMESTAMP,
            phone_number VARCHAR(%(phone_number_length)s),
            pronouns VARCHAR(%(pronouns_length)s),
            sex BOOLEAN,
            gender VARCHAR(%(gender_length)s),
            country VARCHAR(%(country_length)s),
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            updated_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            last_login TIMESTAMP,
            last_login_attempt TIMESTAMP,
            banned BOOLEAN NOT NULL DEFAULT FALSE,
            admin BOOLEAN NOT NULL DEFAULT FALSE,
            avatar_id INT REFERENCES avatars(id)
        );
        """, {
            'username_length': USER_COLUMN_LENGTHS['username'][1],
            'password_length': USER_COLUMN_LENGTHS['password'][1],
            'twofa_secret_length': USER_COLUMN_LENGTHS['twofa_secret'][1],
            'name_length': USER_COLUMN_LENGTHS['name'][1],
            'surname_length': USER_COLUMN_LENGTHS['surname'][1],
            'email_length': USER_COLUMN_LENGTHS['email'][1],
            'description_length': USER_COLUMN_LENGTHS['description'][1],
            'phone_number_length': USER_COLUMN_LENGTHS['phone_number'][1],
            'pronouns_length': USER_COLUMN_LENGTHS['pronouns'][1],
            'gender_length': USER_COLUMN_LENGTHS['gender'][1],
            'country_length': USER_COLUMN_LENGTHS['country'][1]
        })

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
