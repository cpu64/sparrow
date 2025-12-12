from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import models.gallery.image_comment as image_comment_model

image_comments_bp = Blueprint('image_comment', __name__)

@image_comments_bp.route('', methods=['GET'])
def list_image_comments(gallery_id, image_id):
    _ = gallery_id
    image_comments = image_comment_model.get_image_comments()
    return image_comments
