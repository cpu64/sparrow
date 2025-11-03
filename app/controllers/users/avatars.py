# controllers/users/avatars.py
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from models.users.avatar import get_avatars, add, remove, check_length

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
        if (err := check_length('name', name)):
            flash(f"Avatar name must be between {err} characters.", "error")
        elif (err := check_length('url', url)):
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
