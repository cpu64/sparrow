from flask import Blueprint, flash, redirect, render_template, session, url_for
import json

dms_blueprint = Blueprint('dms', __name__)

@dms_blueprint.route('/', methods=['GET'])
def dms():
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    # for now, mock data instead of fetching from database
    # (will also need to fetch user id from session)
    chat_dump = """
    [
        {
            "id": 1,
            "title": "Vienas pokalbis"
        },
        {
            "id": 2,
            "title": "Keistas pokalbis"
        },
        {
            "id": 3,
            "title": "Ne pokalbis"
        }
    ]
    """
    chats = json.loads(chat_dump)

    return render_template('dms/dm_list.html', chats=chats)

@dms_blueprint.route('/chat/<chat_id>', methods=['GET'])
def fetch_chat(chat_id):
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    chat_dump = """
[
    [
        {
            "sender": "A",
            "content": "labas"
        },
        {
            "sender": "B",
            "content": "ate"
        },
        {
            "sender": "A",
            "content": "Nemandagu!"
        }
    ],
    [
        {
            "sender": "A",
            "content": "labas"
        },
        {
            "sender": "A",
            "content": "labas!!!"
        },
        {
            "sender": "B",
            "content": "Nemandagu!"
        }
    ],
    [
        {
            "sender": "A",
            "content": "ate"
        },
        {
            "sender": "B",
            "content": "o kur labas?"
        },
        {
            "sender": "B",
            "content": "sakiau ate"
        },
        {
            "sender": "A",
            "content": "miau"
        }
    ]
]
"""

    messages = json.loads(chat_dump)[int(chat_id) - 1]

    return render_template('dms/chat.html', chat_id=chat_id, messages=messages)
