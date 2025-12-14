# models/users/user.py
from models.db import execute, get_one
from datetime import datetime
import psycopg2

USER_COLUMN_LENGTHS = {
    "username": [3, 30],
    "password": [3, 60],
    "twofa_secret": [3, 40],
    "name": [0, 30],
    "surname": [0, 30],
    "email": [0, 60],
    "description": [0, 1000],
    "phone_number": [0, 20],
    "pronouns": [0, 30],
    "gender": [0, 30],
    "country": [0, 30]
}

def check_length(key, value):
    if USER_COLUMN_LENGTHS[key][0] <= len(value) <= USER_COLUMN_LENGTHS[key][1]:
        return False
    return f"{USER_COLUMN_LENGTHS[key][0]} and {USER_COLUMN_LENGTHS[key][1]}"

def get_username(id):
    data = get_one("""
        SELECT username FROM users WHERE id = %s
        """, (id,))

    return data['username']

def get_data(username, fields):
    try:
        columns_to_select = ', '.join(fields)
        data = get_one(f"""
            SELECT {columns_to_select}
            FROM users WHERE username = %s
        """, (username,))
        if data:
            return data
        return "No such user."

    except Exception as e:
        print(f"Error occurred while fetching user data: {e}")
        return "Error occurred while fetching user data."

def update(username, key, value):
    try:
        execute(f"""
                UPDATE users
                SET {key} = %s, updated_at = %s
                WHERE username = %s;
            """, (value, datetime.utcnow(), username))
    except psycopg2.errors.UniqueViolation:
        print(f"Already exists.")
        return "Already exists."
    except psycopg2.errors.StringDataRightTruncation:
        print(f"Invalid input length.")
        return "Invalid input length."
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."

def toggle(username, key):
    try:
        execute(f"""
            UPDATE users
            SET {key} = NOT {key}, updated_at = %s
            WHERE username = %s;
        """, (datetime.utcnow(), username))
    except psycopg2.errors.UndefinedColumn:
        print(f"Column '{key}' does not exist.")
        return f"Column '{key}' does not exist."
    except psycopg2.errors.DatatypeMismatch:
        print(f"Column '{key}' is not a boolean column.")
        return f"Column '{key}' is not a boolean column."
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."

def toggle_null(username, key, value):
    try:
        execute(f"""
            UPDATE users
            SET {key} = CASE
                            WHEN {key} IS NULL THEN %s
                            ELSE NULL
                         END,
                updated_at = %s
            WHERE username = %s;
        """, (value, datetime.utcnow(), username))
    except psycopg2.errors.UndefinedColumn:
        print(f"Column '{key}' does not exist.")
        return f"Column '{key}' does not exist."
    except psycopg2.errors.DatatypeMismatch:
        print(f"Column '{key}' is not of the expected data type: {data_type}.")
        return f"Column '{key}' is not of the expected data type: {data_type}."
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."

def get_credentials(username):
    try:
        credentials = get_one("SELECT password, admin, twofa_secret, last_login, banned FROM users WHERE username = %s", (username,))
        if credentials:
            return credentials
        return "No such user."
    except Exception as e:
        print(f"Error occurred while fetching user credentials: {e}")
        return "Error occurred while fetching user credentials."

def mark_login(username, successful):
    try:
        current_time = datetime.utcnow()
        if successful:
            execute("""
                UPDATE users
                SET last_login = %s, last_login_attempt = %s
                WHERE username = %s;
            """, (current_time, current_time, username))
        else:
            execute("""
                UPDATE users
                SET last_login_attempt = %s
                WHERE username = %s;
            """, (current_time, username))

    except Exception as e:
        print(f"Error occurred while updating login data: {e}")
        return "Error occurred while updating login data."

def register_user(username, hashed_password):
    try:
        execute("""
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """, (username, hashed_password))
    except psycopg2.errors.UniqueViolation:
        return "Username already exists."

    except psycopg2.errors.StringDataRightTruncation:
        return "Invalid input length. Please check your username and password."

    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."
