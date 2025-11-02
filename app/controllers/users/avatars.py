# controllers/users/avatars.py
from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from models.users.avatar import get_avatars

avatars_bp = Blueprint('avatars', __name__)

@avatars_bp.route('/avatars', methods=['GET', 'POST'])
def avatars():
    if session.get('role', 'guest') != 'admin':
        flash(f"You do not have permisions to access that page.", "error")
        return redirect(url_for('home.home'))
    avatars = get_avatars()
    return render_template('users/avatars.html', avatars=avatars)

@avatars_bp.route('/remove_avatar', methods=['POST'])
def remove_avatar():
    name = request.form.get('avatar_name')
    flash(f"Removed avatar: {name}", "success")
    return redirect(url_for('avatars.avatars'))
