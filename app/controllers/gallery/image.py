from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import models.gallery.image as image_model
import models.gallery.image_comment as comment_model

image_bp = Blueprint('image', __name__)

@image_bp.route('', methods=['GET'])
def list_images(gallery_id):
    images = image_model.get_images()
    return images

@image_bp.route('/<image_id>', methods=['GET'])
def retrieve_image(gallery_id, image_id):
    _ = gallery_id
    image = image_model.get_image()
    comments = comment_model.get_image_comments()
    return render_template('gallery/image.html', image=image, comments=comments)
