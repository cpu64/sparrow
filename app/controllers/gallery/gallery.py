from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import models.gallery.gallery as gallery_model

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('', methods=['GET'])
def list_galleries():
    # TODO: add optional filtering by user_id query parameter (will be used to filter your own galleries)
    galleries = gallery_model.get_galleries()
    return galleries

@gallery_bp.route('/<gallery_id>', methods=['GET'])
def retrieve_gallery(gallery_id):
    gallery = gallery_model.get_gallery()
    return gallery
