# controllers/users/logout.py
from flask import Blueprint, session, redirect, url_for, flash

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.clear()
        flash("Logged out successfully.", 'success')
    return redirect(url_for('login.login'))
