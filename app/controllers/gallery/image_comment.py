from flask import Blueprint, redirect, url_for, session, flash, request
import models.gallery.image_comment as comment_model
from models.users.user import get_data

image_comments_bp = Blueprint('image_comment', __name__)

@image_comments_bp.route('/create', methods=['POST'])
def create_comment(gallery_id, image_id):
    if session.get('role') == 'guest':
        flash("You must be logged in to comment", "error")
        return redirect(url_for('login.login'))

    text = request.form.get('comment_text', '').strip()

    if not text or len(text) < comment_model.COMMENT_COLUMN_LENGTHS['text'][0] or len(text) > comment_model.COMMENT_COLUMN_LENGTHS['text'][1]:
        flash(f"Comment must be between {comment_model.COMMENT_COLUMN_LENGTHS['text'][0]} and {comment_model.COMMENT_COLUMN_LENGTHS['text'][1]} characters", "error")
        return redirect(url_for('image.retrieve_image', gallery_id=gallery_id, image_id=image_id))

    user_data = get_data(session['username'], ['id'])
    if isinstance(user_data, str):
        flash(user_data, "error")
        return redirect(url_for('image.retrieve_image', gallery_id=gallery_id, image_id=image_id))

    try:
        comment_model.create_comment(text, user_data['id'], image_id)
        flash("Comment posted successfully", "success")
    except Exception as e:
        flash(f"Error posting comment: {str(e)}", "error")

    return redirect(url_for('image.retrieve_image', gallery_id=gallery_id, image_id=image_id))
