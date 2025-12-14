from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import models.gallery.gallery as gallery_model
import models.gallery.image as image_model
import models.gallery.image_comment as comment_model
from models.users.user import get_data
from google.cloud import storage
import os
import uuid

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('', methods=['GET'])
def list_galleries():
    view = request.args.get('view', 'my' if session.get('role') != 'guest' else 'all')

    if view == 'my' and session.get('role') != 'guest':
        user_data = get_data(session['username'], ['id'])
        if isinstance(user_data, str):
            flash(user_data, "error")
            return redirect(url_for('gallery.list_galleries', view='all'))
        galleries = gallery_model.get_all_galleries(user_data['id'])
    else:
        galleries = gallery_model.get_all_galleries()
        view = 'all'

    return render_template('gallery/galleries.html', galleries=galleries, current_view=view)

@gallery_bp.route('/<int:gallery_id>', methods=['GET'])
def retrieve_gallery(gallery_id):
    gallery = gallery_model.get_gallery_by_id(gallery_id)
    if not gallery:
        flash("Gallery not found", "error")
        return redirect(url_for('gallery.list_galleries'))
    images = image_model.get_images_by_gallery(gallery_id)
    return render_template('gallery/gallery.html', gallery=gallery, images=images)

@gallery_bp.route('/create', methods=['POST'])
def create_gallery():
    if session.get('role') == 'guest':
        flash("You must be logged in to create a gallery", "error")
        return redirect(url_for('login.login'))

    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    background_color = request.form.get('background_color', '#00aa55')

    if not name or len(name) < gallery_model.GALLERY_COLUMN_LENGTHS['name'][0] or len(name) > gallery_model.GALLERY_COLUMN_LENGTHS['name'][1]:
        flash(f"Gallery name must be between {gallery_model.GALLERY_COLUMN_LENGTHS['name'][0]} and {gallery_model.GALLERY_COLUMN_LENGTHS['name'][1]} characters", "error")
        return redirect(url_for('gallery.list_galleries'))

    if len(description) > gallery_model.GALLERY_COLUMN_LENGTHS['description'][1]:
        flash(f"Description must not exceed {gallery_model.GALLERY_COLUMN_LENGTHS['description'][1]} characters", "error")
        return redirect(url_for('gallery.list_galleries'))

    user_data = get_data(session['username'], ['id'])
    if isinstance(user_data, str):
        flash(user_data, "error")
        return redirect(url_for('gallery.list_galleries'))

    try:
        gallery_id = gallery_model.create_gallery(name, description, background_color, user_data['id'])
        flash("Gallery created successfully", "success")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))
    except Exception as e:
        flash(f"Error creating gallery: {str(e)}", "error")
        return redirect(url_for('gallery.list_galleries'))

@gallery_bp.route('/<int:gallery_id>/delete', methods=['POST'])
def delete_gallery(gallery_id):
    if session.get('role') == 'guest':
        flash("You must be logged in to delete a gallery", "error")
        return redirect(url_for('login.login'))

    user_data = get_data(session['username'], ['id', 'admin'])
    if isinstance(user_data, str):
        flash(user_data, "error")
        return redirect(url_for('gallery.list_galleries'))

    if not user_data['admin'] and not gallery_model.check_owner(gallery_id, user_data['id']):
        flash("You don't have permission to delete this gallery", "error")
        return redirect(url_for('gallery.retrieve_gallery', gallery_id=gallery_id))

    try:
        gallery_model.delete_gallery(gallery_id)
        flash("Gallery deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting gallery: {str(e)}", "error")

    return redirect(url_for('gallery.list_galleries'))

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
