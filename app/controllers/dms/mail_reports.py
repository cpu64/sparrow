import os
import smtplib
from email.message import EmailMessage
import threading
import time

from models.dms.chat import get_all_users, get_chats_with_unseen_messages

def send_email(to_email, subject, body):
    gmail_user = os.environ.get("GMAIL_ADDRESS")
    gmail_pass = os.environ.get("GMAIL_APP_PASSWORD")

    if not gmail_user or not gmail_pass:
        raise RuntimeError("Missing Gmail credentials in environment variables")

    msg = EmailMessage()
    msg["From"] = gmail_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(gmail_user, gmail_pass)
        server.send_message(msg)

def email_users_with_unseen_messages():
    users = get_all_users()

    for user in users:
        user_id = user["id"]
        email = user["email"]

        chats = get_chats_with_unseen_messages(user_id)

        if not chats:
            continue

        lines = [
            "You have unread messages in the following chats:\n"
        ]

        for chat in chats:
            lines.append(
                f"- {chat['name']} ({chat['unseen_count']} unread)"
            )

        body = "\n".join(lines)

        send_email(
            to_email=email,
            subject="You have unread messages",
            body=body
        )

def email_notification_loop(app, interval_seconds=60):
    with app.app_context():
        print("Email notification loop started")

        while True:
            try:
                email_users_with_unseen_messages()
            except Exception as e:
                print("Email notification loop error:", e)

            time.sleep(interval_seconds)

def start_email_loop(app):
    thread = threading.Thread(
        target=email_notification_loop,
        args=(app, 60),
        daemon=True
    )
    thread.start()
