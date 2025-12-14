from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.users.user import get_data, check_length, update, toggle, toggle_null, register_user, get_credentials, mark_login
from models.users.avatar import get_avatar, get_avatars, add, remove, check_length as check_length_avatar
from datetime import datetime, timedelta
from totp import generate_secret, totp_url, totp_qr, verify, period
import bcrypt

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if (err := check_length('username', username)):
            flash(f"Username must be between {err} characters.", "error")
            return render_template('users/register.html')

        if (err := check_length('password', password)):
            flash(f"Password must be between {err} characters.", "error")
            return render_template('users/register.html')

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        if (err := register_user(username, hashed)):
            flash(err, "error")
        else:
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login.login'))

    return render_template('users/register.html')

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('role', 'guest') != 'guest':
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        totp = request.form.get('totp')


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

        if response['banned']:
            if (err := mark_login(username, False)):
                flash(err, "error")
            flash('You have been banned.', "error")
            return render_template('users/login.html')

        password_is_valid = bcrypt.checkpw(password.encode('utf-8'), response['password'].encode('utf-8'))
        response['last_login'] = response['last_login'] if response['last_login'] else datetime.utcfromtimestamp(0)
        new_totp = datetime.utcnow() - response['last_login'] > timedelta(seconds=period)
        twofa_is_valid = not response['twofa_secret'] or (new_totp and verify(totp, response['twofa_secret']))

        if password_is_valid and twofa_is_valid:
            if (err := mark_login(username, True)):
                flash(err, "error")
                return render_template('users/login.html')
            session['username'] = username
            session['role'] = 'admin' if response['admin'] else 'user'
            session['user_id'] = get_data(username, ('id',))['id']
            return redirect(url_for('home.home'))
        if new_totp:
            flash("Invalid credentials, please try again.", "error")
        else:
            flash(f"The 2FA code has been used up, wait {period}s.", "error")
        if (err := mark_login(username, False)):
            flash(err, "error")
            return render_template('users/login.html')

    return render_template('users/login.html')

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if session.get('role', '') != 'guest':
        session.clear()
        flash("Logged out successfully.", 'success')
    else:
        flash("You are not logged in.", 'info')
    return redirect(url_for('login.login'))

profile_bp = Blueprint('profile', __name__)

fields = ['username', 'password', 'name', 'surname', 'email', 'description', 'sex', 'gender', 'pronouns', 'date_of_birth', 'phone_number', 'country', 'created_at', 'updated_at', 'last_login', 'banned', 'admin']

@profile_bp.route('/<user>', methods=['GET', 'POST'])
def profile(user):
    if request.method == 'GET':
        data = get_data(user, fields + ['twofa_secret'])
        if isinstance(data, str):
            return data

        avatar = get_avatar(user)
        data['avatar'] = avatar if not isinstance(avatar, str) else None
        data['owner'] = (session.get('username') == data.get('username', ''))
        data['viewer'] = session.get('role', 'guest')
        data['fields'] = fields
        if data['owner']:
            data['avatars'] = get_avatars()
            data['twofa_qr'] = totp_qr(totp_url(data.get('username', ''), data.get('twofa_secret', '')))

        return render_template('users/profile.html', data=data)

    elif request.method == 'POST':
        field = request.form.get('field')

        if field == 'toggle_ban':
            if session.get('role', 'guest') != 'admin':
                flash(f"You do not have permission to ban/unban people.", "error")
            elif (err := toggle(user, 'banned')):
                flash(f"{field.replace('_', ' ').capitalize()}: {err}", "error")
            return redirect(url_for('profile.profile', user=user))

        if session.get('username') != user:
            flash(f"You do not have permissions to edit this profile.", "error")
            return redirect(url_for('profile.profile', user=user))

        if field in ['name', 'surname', 'email', 'description', 'gender', 'pronouns', 'phone_number', 'country']:
            value = request.form.get(field)
            if (err := check_length(field, value)):
                flash(f"{field.replace('_', ' ').capitalize()} must be between {err} characters.", "error")
            elif (err := update(session.get('username'), field, value)):
                flash(f"{field.replace('_', ' ').capitalize()}: {err}", "error")
        elif field in ['avatar_id', 'date_of_birth']:
            value = request.form.get(field)
            if (err := update(session.get('username'), field, value)):
                flash(f"{field.replace('_', ' ').capitalize()}: {err}", "error")
        elif field == 'username':
            value = request.form.get(field)
            if (err := check_length(field, value)):
                flash(f"{field.replace('_', ' ').capitalize()} must be between {err} characters.", "error")
            elif (err := update(session.get('username'), field, value)):
                flash(f"{field.replace('_', ' ').capitalize()}: {err}", "error")
            else:
                session['username'] = value
                return redirect(url_for('profile.profile', user=value))
        elif field == 'password':
            value = request.form.get(field)
            if (err := check_length(field, value)):
                flash(f"{field.replace('_', ' ').capitalize()} must be between {err} characters.", "error")
            elif (err := update(session.get('username'), field, bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))):
                flash(f"{field.replace('_', ' ').capitalize()}: {err}", "error")
        elif field == 'sex':
            value = request.form.get(field)
            if value == 0 or value == 1:
                flash(f"{field.replace('_', ' ').capitalize()} must be 1 or 0.", "error")
            elif (err := update(session.get('username'), field, value)):
                flash(f"{field.replace('_', ' ').capitalize()}: {err}", "error")
        elif field == 'toggle_2fa':
            if (err := toggle_null(session.get('username'), 'twofa_secret', generate_secret())):
                flash(f"{field.replace('_', ' ').capitalize()}: {err}", "error")
        elif field == 'twofa_secret':
            if (err := update(session.get('username'), field, generate_secret())):
                flash(f"{field.replace('_', ' ').capitalize()}: {err}", "error")
        return redirect(url_for('profile.profile', user=user))

avatars_bp = Blueprint('avatars', __name__)

@avatars_bp.route('/avatars', methods=['GET', 'POST'])
def avatars():
    if session.get('role', 'guest') != 'admin':
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    avatars = get_avatars()
    if request.method == 'GET':
        return render_template('users/avatars.html', avatars=avatars)
    elif request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        if (err := check_length_avatar('name', name)):
            flash(f"Avatar name must be between {err} characters.", "error")
        elif (err := check_length_avatar('url', url)):
            flash(f"Avatar URL must be between {err} characters.", "error")
        elif (err := add(name, url)):
            flash(f"{err}", "error")
        return redirect(url_for('avatars.avatars'))

@avatars_bp.route('/remove_avatar', methods=['POST'])
def remove_avatar():
    if session.get('role', 'guest') != 'admin':
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))

    name = request.form.get('avatar_name')
    if (err := remove(name)):
        flash(f"{err}", "error")
    else:
        flash(f"Removed avatar: {name}", "success")
    return redirect(url_for('avatars.avatars'))
