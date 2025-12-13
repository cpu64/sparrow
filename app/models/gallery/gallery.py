from models.db import execute, get_one, get_all
from datetime import datetime

GALLERY_COLUMN_LENGTHS = {
    "name": [1, 255],
    "description": [0, 500],
    "background_color": [0, 255]
}

def get_all_galleries(user_id=None):
    query = """
        SELECT g.id, g.name, g.description, g.created_at, g.updated_at, g.background_color,
               u.username as owner, a.url as owner_avatar
        FROM galleries g
        JOIN users u ON g.user_id = u.id
        LEFT JOIN avatars a ON u.avatar_id = a.id
    """
    if user_id:
        return get_all(query + " WHERE g.user_id = %s ORDER BY g.updated_at DESC", (user_id,))
    return get_all(query + " ORDER BY g.updated_at DESC")

def get_gallery_by_id(gallery_id):
    return get_one("""
        SELECT g.id, g.name, g.description, g.created_at, g.updated_at, g.background_color,
               u.username as owner, a.url as owner_avatar
        FROM galleries g
        JOIN users u ON g.user_id = u.id
        LEFT JOIN avatars a ON u.avatar_id = a.id
        WHERE g.id = %s
    """, (gallery_id,))

def create_gallery(name, description, background_color, user_id):
    return execute("""
        INSERT INTO galleries (name, description, background_color, user_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (name, description, background_color, user_id, datetime.utcnow(), datetime.utcnow()))

def delete_gallery(gallery_id):
    execute("DELETE FROM galleries WHERE id = %s", (gallery_id,))

def update_gallery_timestamp(gallery_id):
    execute("UPDATE galleries SET updated_at = %s WHERE id = %s", (datetime.utcnow(), gallery_id))

def check_owner(gallery_id, user_id):
    result = get_one("SELECT user_id FROM galleries WHERE id = %s", (gallery_id,))
    return result and result['user_id'] == user_id
