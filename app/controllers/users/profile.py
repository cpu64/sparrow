# controllers/users/profile.py
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from models.users.user import get_data, check_length, update, toggle, toggle_null
from models.users.avatar import get_avatar, get_avatars
from totp import generate_secret, totp_url, totp_qr
import bcrypt

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
