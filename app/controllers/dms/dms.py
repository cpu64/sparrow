from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for
from models.dms.message import create_message, update_message_contents
from models.users.avatar import get_avatar
from models.dms.chat import create_new_chat, get_chat_name, list_chats_for_user, get_messages_for_chat, mark_chat_messages_as_seen
from models.users.user import get_data, get_username

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

def get_messages(chat_id):
    user_id = session.get("user_id")

    mark_chat_messages_as_seen(chat_id, user_id)

    messages = get_messages_for_chat(chat_id)
    messages = [{
        'sender': get_username(m['sender_id']),
        'sender_avatar': get_avatar(get_username(m['sender_id']))['url'],
        'content': m['text'],
        'sent_by_me': m['sender_id'] == user_id,
        'id': m['id']
                 } for m in messages]
    return messages

@dms_blueprint.route('/chat/<chat_id>', methods=['GET'])
def fetch_chat(chat_id):
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    messages = get_messages(chat_id)

    return render_template('dms/chat.html', chat_name=get_chat_name(chat_id), chat_id=chat_id, messages=messages)

@dms_blueprint.route("/fetch_chat/<chat_id>", methods=['GET'])
def fetch_chat_messages(chat_id):
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    messages = get_messages(chat_id)

    return jsonify(messages)

@dms_blueprint.route('/new_chat', methods=['GET'])
def new_chat():
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    return render_template('dms/new_chat.html')

@dms_blueprint.route('/create_chat', methods=['POST'])
def create_chat():
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    username = request.form.get('username')
    chat_name = request.form.get('chat_name')

    if username == None or chat_name == None or username == "" or chat_name == "":
        flash(f"Form is missing required fields. Please fill in a valid chat name and username.", "error")
        return redirect(url_for('dms.new_chat'))

    other_user_query = get_data(username, ('id',))
    if other_user_query in ["No such user.", "Error occurred while fetching user data."]:
        flash(f"Invalid username. {other_user_query}", "error")
        return redirect(url_for('dms.new_chat'))

    other_id = other_user_query['id']
    current_id = session.get("user_id")

    if current_id == other_id:
        flash(f"Cannot invite yourself into a chat.", "error")
        return redirect(url_for('dms.new_chat'))

    create_new_chat(chat_name, other_id, current_id)

    return redirect(url_for('dms.dms'))

@dms_blueprint.route('/edit_message/<message_id>', methods=['POST'])
def edit_message(message_id):
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    data = request.get_json(silent=True)
    if not data or "content" not in data:
        return jsonify({"error": "Missing content"}), 400

    new_text = data["content"].strip()
    if not new_text:
        return jsonify({"error": "Message cannot be empty"}), 400

    update_message_contents(message_id, new_text)

    return jsonify({"status": "ok"})

@dms_blueprint.route('/send_message/<chat_id>', methods=['POST'])
def send_message(chat_id):
    role = session.get("role", "")
    if role == "guest":
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    data = request.get_json(silent=True)
    if not data or "content" not in data:
        return jsonify({"error": "Missing content"}), 400

    new_text = data["content"].strip()
    if not new_text:
        return jsonify({"error": "Message cannot be empty"}), 400

    user_id = session.get("user_id")
    create_message(chat_id, user_id, new_text)

    return jsonify({"status": "ok"})
