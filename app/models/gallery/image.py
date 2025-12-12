from models.db import execute, get_one, get_all
from datetime import datetime

IMAGE_COLUMN_LENGTHS = {
    "name": [1, 255],
    "url": [1, 255],
    "description": [0, 255],
    "location": [0, 255]
}

def get_images_by_gallery(gallery_id):
    return get_all("""
        SELECT id, name, url, description, location, taken_at, created_at
        FROM images
        WHERE gallery_id = %s
        ORDER BY created_at DESC
    """, (gallery_id,))

def get_image_by_id(image_id):
    return get_one("""
        SELECT id, name, url, description, location, taken_at, created_at, gallery_id
        FROM images
        WHERE id = %s
    """, (image_id,))

def create_image(name, url, description, location, taken_at, gallery_id):
    execute("""
        INSERT INTO images (name, url, description, location, taken_at, gallery_id, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (name, url, description, location, taken_at, gallery_id, datetime.utcnow()))

def delete_image(image_id):
    execute("DELETE FROM images WHERE id = %s", (image_id,))

def check_owner_by_image(image_id, user_id):
    result = get_one("""
        SELECT g.user_id
        FROM images i
        JOIN galleries g ON i.gallery_id = g.id
        WHERE i.id = %s
    """, (image_id,))
    return result and result['user_id'] == user_id
