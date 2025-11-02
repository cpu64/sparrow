# models/users/avatar.py
from models.db import get_one, get_all, execute
import psycopg2

AVATAR_COLUMN_LENGTHS = {
    "name": [3, 30],
    "url": [3, 2147483647]
}

def check_length(key, value):
    if AVATAR_COLUMN_LENGTHS[key][0] <= len(value) <= AVATAR_COLUMN_LENGTHS[key][1]:
        return False
    return f"{AVATAR_COLUMN_LENGTHS[key][0]} and {AVATAR_COLUMN_LENGTHS[key][1]}"

def add(name, url):
    try:
        execute("""
            INSERT INTO avatars (name, url)
            VALUES (%s, %s)
        """, (name, url))
    except psycopg2.errors.UniqueViolation:
        return "Name or URL already exists."

    except psycopg2.errors.StringDataRightTruncation:
        return "Invalid input length. Please check name and URL."

    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."

def remove(name):
    try:
        execute("""
             DELETE FROM avatars WHERE name = %s
        """, (name, ))
    except psycopg2.errors.ForeignKeyViolation:
        return "There are users using this avatar."

    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."

def get_avatar(username):
    try:
        avatar = get_one("""
            SELECT a.name, a.url, a.created_at
            FROM avatars a
            JOIN users u ON u.avatar_id = a.id
            WHERE u.username = %s
        """, (username,))
        if avatar:
            return avatar
        return "No such user or avatar."
    except Exception as e:
        print(f"Error occurred while fetching avatar data: {e}")
        return "Error occurred while fetching avatar data."

def get_avatars():
    try:
        avatars = get_all("""SELECT a.name, a.url, a.id FROM avatars a ORDER BY a.id DESC""")
        if avatars:
            return avatars
        return []
    except Exception as e:
        print(f"Error occurred while fetching avatar data: {e}")
        return "Error occurred while fetching avatar data."
