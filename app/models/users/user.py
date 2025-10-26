# models/users/user.py

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
