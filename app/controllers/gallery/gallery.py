from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import models.gallery.gallery as gallery_model
import models.gallery.image as image_model
from models.users.user import get_data

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
        gallery_model.create_gallery(name, description, background_color, user_data['id'])
        flash("Gallery created successfully", "success")
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
