from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import models.gallery.image as image_model
import models.gallery.image_comment as comment_model
import models.gallery.gallery as gallery_model
from models.users.user import get_data
from google.cloud import storage
import os
import uuid

image_bp = Blueprint('image', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}

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

    file = request.files.get('file')
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    location = request.form.get('location', '').strip()
    taken_at = request.form.get('taken_at') or None

    if not file or file.filename == '':
        flash("No file selected", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if '.' not in file.filename:
        flash("File must have an extension", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    ext = file.filename.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        flash(f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if not name or len(name) < image_model.IMAGE_COLUMN_LENGTHS['name'][0] or len(name) > image_model.IMAGE_COLUMN_LENGTHS['name'][1]:
        flash(f"Image name must be between {image_model.IMAGE_COLUMN_LENGTHS['name'][0]} and {image_model.IMAGE_COLUMN_LENGTHS['name'][1]} characters", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if len(description) > image_model.IMAGE_COLUMN_LENGTHS['description'][1]:
        flash(f"Description must not exceed {image_model.IMAGE_COLUMN_LENGTHS['description'][1]} characters", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    if len(location) > image_model.IMAGE_COLUMN_LENGTHS['location'][1]:
        flash(f"Location must not exceed {image_model.IMAGE_COLUMN_LENGTHS['location'][1]} characters", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(os.getenv('GCS_BUCKET_NAME'))

        unique_filename = f"{uuid.uuid4()}.{ext}"
        blob = bucket.blob(f"images/{unique_filename}")

        file.seek(0)
        blob.upload_from_file(file, content_type=file.content_type)
        gcs_url = blob.public_url

        image_model.create_image(name, gcs_url, description, location, taken_at, gallery_id)
        gallery_model.update_gallery_timestamp(gallery_id)
        flash("Image uploaded successfully", "success")
    except Exception as e:
        flash(f"Failed to upload image: {str(e)}", "error")

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
