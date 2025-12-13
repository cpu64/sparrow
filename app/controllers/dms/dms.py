from flask import Blueprint, flash, redirect, render_template, session, url_for
from models.users.avatar import get_avatar
from models.dms.chat import get_chat_name, list_chats_for_user, get_messages_for_chat
from models.users.user import get_username

dms_blueprint = Blueprint('dms', __name__)

@dms_blueprint.route('/', methods=['GET'])
def dms():
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    user_id = session.get("user_id")
    chats = list_chats_for_user(user_id)

    return render_template('dms/dm_list.html', chats=chats)

@dms_blueprint.route('/chat/<chat_id>', methods=['GET'])
def fetch_chat(chat_id):
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    user_id = session.get("user_id")
    messages = get_messages_for_chat(chat_id)
    messages = [{
        'sender': get_username(m.sender_id),
        'sender_avatar': get_avatar(get_username(m.sender_id))['url'],
        'content': m.text,
        'sent_by_me': m.sender_id == user_id,
        'id': m.id
                 } for m in messages]

    return render_template('dms/chat.html', chat_name=get_chat_name(chat_id), messages=messages)

@dms_blueprint.route('/new_chat', methods=['GET'])
def new_chat():
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    return render_template('dms/new_chat.html')
