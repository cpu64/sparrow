# controllers/users/login.py
import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.users.user import check_length, get_credentials, mark_login

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')


        if (err := check_length('username', username)):
            flash(f"Username must be between {err} characters.", "error")
            return render_template('users/login.html')

        if (err := check_length('password', password)):
            flash(f"Password must be between {err} characters.", "error")
            return render_template('users/login.html')

        response = get_credentials(username)

        if isinstance(response, str):
            flash(response, "error")
            return render_template('users/login.html')

        if bcrypt.checkpw(password.encode('utf-8'), response['password'].encode('utf-8')):
            if (err := mark_login(username, True)):
                flash(err, "error")
                return render_template('users/login.html')
            session['username'] = username
            session['role'] = 'admin' if response['admin'] else 'user'
            return redirect(url_for('home.home'))

        flash("Invalid credentials, please try again.", "error")
        if (err := mark_login(username, False)):
            flash(err, "error")
            return render_template('users/login.html')

    return render_template('users/login.html')
