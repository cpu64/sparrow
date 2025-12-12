from models.db import execute, get_all
from datetime import datetime

COMMENT_COLUMN_LENGTHS = {
    "text": [1, 255]
}

def get_comments_by_image(image_id):
    return get_all("""
        SELECT c.id, c.text, c.created_at, u.username as author, a.url as author_avatar
        FROM image_comments c
        JOIN users u ON c.user_id = u.id
        LEFT JOIN avatars a ON u.avatar_id = a.id
        WHERE c.image_id = %s
        ORDER BY c.created_at DESC
    """, (image_id,))

def create_comment(text, user_id, image_id):
    execute("""
        INSERT INTO image_comments (text, user_id, image_id, created_at)
        VALUES (%s, %s, %s, %s)
    """, (text, user_id, image_id, datetime.utcnow()))
