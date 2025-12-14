from models.db import get_one, get_all, execute
import psycopg2

COMMENT_COLUMN_LENGTHS = {"content": [1, 500]}


def check_length(key, value):
    if COMMENT_COLUMN_LENGTHS[key][0] <= len(value) <= COMMENT_COLUMN_LENGTHS[key][1]:
        return False
    return f"{COMMENT_COLUMN_LENGTHS[key][0]} and {COMMENT_COLUMN_LENGTHS[key][1]}"


def get_comments(post_id):
    try:
        comments = get_all(
            """
            SELECT c.id, c.content AS text, c.created_at,
                   u.username AS author
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.post_id = %s
            ORDER BY c.created_at DESC
        """,
            (post_id,),
        )
        if comments:
            return comments
        return []
    except Exception as e:
        print(f"Error occurred while fetching comments data: {e}")
        return "Error occurred while fetching comments data."


def get_comment(comment_id):
    try:
        comment = get_one(
            """
            SELECT c.id, c.content, c.created_at,
                   u.username AS author
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.id = %s
        """,
            (comment_id,),
        )
        if comment:
            return comment
        return None
    except Exception as e:
        print(f"Error occurred while fetching comment data: {e}")
        return "Error occurred while fetching comment data."


def add_comment(post_id, user_id, content):
    try:
        execute(
            """
            INSERT INTO comments (post_id, user_id, content)
            VALUES (%s, %s, %s)
        """,
            (post_id, user_id, content),
        )
    except psycopg2.errors.StringDataRightTruncation:
        return "Invalid input length. Please check content."
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."


def remove_comment(comment_id):
    try:
        execute(
            """
             DELETE FROM comments WHERE id = %s
        """,
            (comment_id,),
        )
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."
