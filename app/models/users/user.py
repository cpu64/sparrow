# models/users/user.py
from models.db import execute, get_one
from datetime import datetime

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

def get_credentials(username):
    try:
        credentials = get_one("SELECT password, admin, twofa_secret FROM users WHERE username = %s", (username,))
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
