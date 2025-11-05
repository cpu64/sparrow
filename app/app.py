# app.py
from flask import Flask, redirect, url_for, session, flash
from datetime import datetime, timezone, timedelta
from models.db import init_db
from models.users.user import get_data
from controllers.home import home_bp
from controllers.users.login import login_bp
from controllers.users.logout import logout_bp
from controllers.users.avatars import avatars_bp
from controllers.users.profile import profile_bp
from controllers.users.register import register_bp
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(login_bp, url_prefix='/users')
app.register_blueprint(logout_bp, url_prefix='/users')
app.register_blueprint(avatars_bp, url_prefix='/users/')
app.register_blueprint(profile_bp, url_prefix='/users/profile')
app.register_blueprint(register_bp, url_prefix='/users')

@app.before_request
def ensure_default_session():
    if 'role' not in session:
        session['role'] = 'guest'
    if session['role'] != 'guest':
        if 'last_check' in session:
            if datetime.utcnow().replace(tzinfo=timezone.utc) - session['last_check'].replace(tzinfo=timezone.utc) > timedelta(minutes=1):
                data = get_data(session.get('username'), ['banned'])
                if isinstance(data, str):
                    flash(data, "error")
                    return redirect(url_for('login.login'))
                if data['banned']:
                    session.clear()
                    flash('You have been banned.', "error")
                    return redirect(url_for('login.login'))
                session['last_check'] = datetime.utcnow().replace(tzinfo=timezone.utc)
        else:
            session['last_check'] = datetime.fromtimestamp(0, timezone.utc).replace(tzinfo=timezone.utc)

@app.route('/')
def index():
    return redirect(url_for('home.home'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host=os.getenv('FALSK_HOST', '0.0.0.0'), port=os.getenv('FALSK_PORT', '5000'))

