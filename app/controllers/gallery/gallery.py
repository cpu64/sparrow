from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import models.gallery.gallery as gallery_model
import models.gallery.image as image_model

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('', methods=['GET'])
def list_galleries():
    # TODO: add optional filtering by user_id query parameter (will be used to filter your own galleries)
    galleries = gallery_model.get_galleries()
    return render_template('gallery/galleries.html', galleries=galleries)

@gallery_bp.route('/<gallery_id>', methods=['GET'])
def retrieve_gallery(gallery_id):
    gallery = gallery_model.get_gallery()
    images = image_model.get_images()
    return render_template('gallery/gallery.html', gallery=gallery, images=images)
