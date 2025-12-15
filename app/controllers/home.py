# controllers/home.py
from flask import Blueprint, render_template, redirect, url_for, session

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html', username=session.get('username', 'Guest'), role=session.get('role', 'guest'))
