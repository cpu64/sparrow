# models/users/user.py
from models.db import get_db_connection

USER_COLUMN_LENGTHS = {
    "username": [3, 30],
    "password": [3, 60],
    "twofa_secret": [3, 40],
    "name": [1, 30],
    "surname": [1, 30],
    "email": [1, 60],
    "description": [1, 1000],
    "phone_number": [1, 20],
    "pronouns": [1, 30],
    "gender": [1, 30],
    "country": [1, 30]
}

def check_length(key, value):
    if USER_COLUMN_LENGTHS[key][0] <= len(value) <= USER_COLUMN_LENGTHS[key][1]:
        return False
    return f"{USER_COLUMN_LENGTHS[key][0]} and {USER_COLUMN_LENGTHS[key][1]}"

def get_credentials(username):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT password, admin, twofa_secret FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user:
            columns = [desc[0] for desc in cur.description]
            user_dict = dict(zip(columns, user))
            return user_dict
        return "No such user."

    except Exception as e:
        print(f"Error occurred while fetching user credentials: {e}")
        return "Error occurred while fetching user credentials."

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
