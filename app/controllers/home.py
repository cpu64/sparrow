# controllers/home.py
from flask import Blueprint, render_template, redirect, url_for, session

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if session.get('role', 'guest') == 'guest':
        return redirect(url_for('login.login'))
    return render_template('home.html', username=session['username'], role=session['role'])
