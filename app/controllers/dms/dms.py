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
            "sender": "admin",
            "content": "labas",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "aaa",
            "content": "ate",
            "sent_by_me": false,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg/800px-Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"
        },
        {
            "sender": "admin",
            "content": "Nemandagu!",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        }
    ],
    [
        {
            "sender": "admin",
            "content": "labas",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "admin",
            "content": "labas!!!",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "aaa",
            "content": "Nemandagu!",
            "sent_by_me": false,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg/800px-Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"
        },
        {
            "sender": "admin",
            "content": "Daug teksto: Nesu tikras ka cia rasyti ir kodel nenoriu naudoti to lorem ipsum ar kokio ten bieso tai stai istorija apie katina. Katinas buvo mielas. Katinas suvalge suni. Katinas kietas. Katinas mire. Pabaiga.",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "admin",
            "content": "Daug teksto: Nesu tikras ka cia rasyti ir kodel nenoriu naudoti to lorem ipsum ar kokio ten bieso tai stai istorija apie katina. Katinas buvo mielas. Katinas suvalge suni. Katinas kietas. Katinas mire. Pabaiga.",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "admin",
            "content": "Daug teksto: Nesu tikras ka cia rasyti ir kodel nenoriu naudoti to lorem ipsum ar kokio ten bieso tai stai istorija apie katina. Katinas buvo mielas. Katinas suvalge suni. Katinas kietas. Katinas mire. Pabaiga.",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "admin",
            "content": "Daug teksto: Nesu tikras ka cia rasyti ir kodel nenoriu naudoti to lorem ipsum ar kokio ten bieso tai stai istorija apie katina. Katinas buvo mielas. Katinas suvalge suni. Katinas kietas. Katinas mire. Pabaiga.",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "admin",
            "content": "Daug teksto: Nesu tikras ka cia rasyti ir kodel nenoriu naudoti to lorem ipsum ar kokio ten bieso tai stai istorija apie katina. Katinas buvo mielas. Katinas suvalge suni. Katinas kietas. Katinas mire. Pabaiga.",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "admin",
            "content": "Daug teksto: Nesu tikras ka cia rasyti ir kodel nenoriu naudoti to lorem ipsum ar kokio ten bieso tai stai istorija apie katina. Katinas buvo mielas. Katinas suvalge suni. Katinas kietas. Katinas mire. Pabaiga.",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        }
    ],
    [
        {
            "sender": "admin",
            "content": "ate",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "aaa",
            "content": "o kur labas?",
            "sent_by_me": false,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg/800px-Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"
        },
        {
            "sender": "aaa",
            "content": "sakiau ate",
            "sent_by_me": true,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Cat_August_2010-4.jpg/1920px-Cat_August_2010-4.jpg"
        },
        {
            "sender": "aaa",
            "content": "miau",
            "sent_by_me": false,
            "sender_avatar": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg/800px-Orange_tabby_cat_sitting_on_fallen_leaves-Hisashi-01A.jpg"
        }
    ]
]
"""

    messages = json.loads(chat_dump)[int(chat_id) - 1]

    return render_template('dms/chat.html', chat_id=chat_id, messages=messages)

@dms_blueprint.route('/new_chat', methods=['GET'])
def new_chat():
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    return render_template('dms/new_chat.html')
