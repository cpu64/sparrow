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
            "user": 1,
            "sender": "A",
            "content": "labas"
        },
        {
            "user": 2,
            "sender": "B",
            "content": "ate fesgrdg poirkgjdj orjerjoghijerohj gerj perj gpjrpg per gperj pgkpkg poewk pgpwo jgpewj gpwe pojwpej gpewj gpwj pgojewp ogjwpo gjpwej gpwoej gp fesgrdg poirkgjdj orjerjoghijerohj gerj perj gpjrpg per gperj pgkpkg poewk pgpwo jgpewj gpwe pojwpej gpewj gpwj pgojewp ogjwpo gjpwej gpwoej gp"
        },
        {
            "user": 1,
            "sender": "A",
            "content": "Nemandagu!"
        }
    ],
    [
        {
            "user": 1,
            "sender": "A",
            "content": "labas"
        },
        {
            "user": 1,
            "sender": "A",
            "content": "labas!!!"
        },
        {
            "user": 2,
            "sender": "B",
            "content": "Nemandagu!"
        }
    ],
    [
        {
            "user": 1,
            "sender": "A",
            "content": "ate"
        },
        {
            "user": 2,
            "sender": "B",
            "content": "o kur labas?"
        },
        {
            "user": 2,
            "sender": "B",
            "content": "sakiau ate"
        },
        {
            "user": 1,
            "sender": "A",
            "content": "miau"
        }
    ]
]
"""

    messages = json.loads(chat_dump)[int(chat_id) - 1]

    return render_template('dms/chat.html', chat_id=chat_id, messages=messages)
