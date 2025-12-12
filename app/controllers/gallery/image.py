from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import models.gallery.image as image_model
import models.gallery.image_comment as comment_model
import models.gallery.gallery as gallery_model
from models.users.user import get_data

image_bp = Blueprint('image', __name__)

@image_bp.route('/<int:image_id>', methods=['GET'])
def retrieve_image(gallery_id, image_id):
    image = image_model.get_image_by_id(image_id)
    if not image:
        flash("Image not found", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))
    comments = comment_model.get_comments_by_image(image_id)
    return render_template('gallery/image.html', image=image, comments=comments, gallery_id=gallery_id)

@image_bp.route('/create', methods=['POST'])
def create_image(gallery_id):
    if session.get('role') == 'guest':
        flash("You must be logged in to upload an image", "error")
        return redirect(url_for('login.login'))

    user_data = get_data(session['username'], ['id'])
    if isinstance(user_data, str):
        flash(user_data, "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if not gallery_model.check_owner(gallery_id, user_data['id']):
        flash("You don't have permission to add images to this gallery", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    name = request.form.get('name', '').strip()
    url = request.form.get('url', '').strip()
    description = request.form.get('description', '').strip()
    location = request.form.get('location', '').strip()
    taken_at = request.form.get('taken_at') or None

    if not name or len(name) < image_model.IMAGE_COLUMN_LENGTHS['name'][0] or len(name) > image_model.IMAGE_COLUMN_LENGTHS['name'][1]:
        flash(f"Image name must be between {image_model.IMAGE_COLUMN_LENGTHS['name'][0]} and {image_model.IMAGE_COLUMN_LENGTHS['name'][1]} characters", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if not url or len(url) < image_model.IMAGE_COLUMN_LENGTHS['url'][0] or len(url) > image_model.IMAGE_COLUMN_LENGTHS['url'][1]:
        flash(f"Image URL must be between {image_model.IMAGE_COLUMN_LENGTHS['url'][0]} and {image_model.IMAGE_COLUMN_LENGTHS['url'][1]} characters", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if len(description) > image_model.IMAGE_COLUMN_LENGTHS['description'][1]:
        flash(f"Description must not exceed {image_model.IMAGE_COLUMN_LENGTHS['description'][1]} characters", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if len(location) > image_model.IMAGE_COLUMN_LENGTHS['location'][1]:
        flash(f"Location must not exceed {image_model.IMAGE_COLUMN_LENGTHS['location'][1]} characters", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    try:
        image_model.create_image(name, url, description, location, taken_at, gallery_id)
        gallery_model.update_gallery_timestamp(gallery_id)
        flash("Image uploaded successfully", "success")
    except Exception as e:
        flash(f"Error uploading image: {str(e)}", "error")

    return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

@image_bp.route('/<int:image_id>/delete', methods=['POST'])
def delete_image(gallery_id, image_id):
    if session.get('role') == 'guest':
        flash("You must be logged in to delete an image", "error")
        return redirect(url_for('login.login'))

    user_data = get_data(session['username'], ['id', 'admin'])
    if isinstance(user_data, str):
        flash(user_data, "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if not user_data['admin'] and not image_model.check_owner_by_image(image_id, user_data['id']):
        flash("You don't have permission to delete this image", "error")
        return redirect(url_for('image.retrieve_image', gallery_id=gallery_id, image_id=image_id))

    try:
        image_model.delete_image(image_id)
        gallery_model.update_gallery_timestamp(gallery_id)
        flash("Image deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting image: {str(e)}", "error")

    return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))
