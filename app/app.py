# app.py
from flask import Flask, redirect, url_for, session
from models.db import init_db
from controllers.home import home_bp
from controllers.users.login import login_bp
from controllers.users.logout import logout_bp
from controllers.users.register import register_bp
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(login_bp, url_prefix='/users')
app.register_blueprint(logout_bp, url_prefix='/users')
app.register_blueprint(register_bp, url_prefix='/users')

@app.before_request
def ensure_default_session():
    if 'role' not in session:
        session['role'] = 'guest'

@app.route('/')
def index():
    return redirect(url_for('home.home'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host=os.getenv('FALSK_HOST', '0.0.0.0'), port=os.getenv('FALSK_PORT', '5000'))

