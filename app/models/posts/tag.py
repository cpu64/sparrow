from models.db import get_one, get_all, execute
import psycopg2

TAG_COLUMN_LENGTHS = {"name": [1, 63]}


def check_length(key, value):
    if TAG_COLUMN_LENGTHS[key][0] <= len(value) <= TAG_COLUMN_LENGTHS[key][1]:
        return False
    return f"{TAG_COLUMN_LENGTHS[key][0]} and {TAG_COLUMN_LENGTHS[key][1]}"


def check_exists(name):
    try:
        tag = get_one(
            """
            SELECT id FROM tags WHERE name = %s
        """,
            (name,),
        )
        if tag:
            return True
        return False
    except Exception as e:
        print(f"Error occurred while checking tag existence: {e}")
        return "Error occurred while checking tag existence."


def get_tag_id(name):
    try:
        tag = get_one(
            """
            SELECT id FROM tags WHERE name = %s
        """,
            (name,),
        )
        if tag:
            return tag["id"]
        return None
    except Exception as e:
        print(f"Error occurred while fetching tag ID: {e}")
        return "Error occurred while fetching tag ID."


def add(name, date):
    try:
        if date is None:
            date = "NOW()"
        tag_id = get_one(
            """
            INSERT INTO tags (name, created_at)
            VALUES (%s, %s)
            RETURNING id
        """,
            (name, date),
            commit=True,
        )
        if tag_id:
            return tag_id["id"]
    except psycopg2.errors.UniqueViolation:
        return "Tag name already exists."
    except psycopg2.errors.StringDataRightTruncation:
        return "Invalid input length. Please check name."
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."


def add_post_tag(post_id, tag_id):
    try:
        execute(
            """
            INSERT INTO post_tags (post_id, tag_id)
            VALUES (%s, %s)
        """,
            (post_id, tag_id),
        )
    except psycopg2.errors.UniqueViolation:
        return "Post tag association already exists."
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."


def get_tags_for_post(post_id):
    try:
        tags = get_all(
            """
            SELECT t.id, t.name
            FROM tags t
            JOIN post_tags pt ON t.id = pt.tag_id
            WHERE pt.post_id = %s
        """,
            (post_id,),
        )
        if tags:
            return tags
        return []
    except Exception as e:
        print(f"Error occurred while fetching tags for post: {e}")
        return "Error occurred while fetching tags for post."


def delete_tag(tag_id):
    try:
        execute(
            """
            DELETE FROM tags WHERE id = %s
        """,
            (tag_id,),
        )
    except Exception as e:
        print(f"Unknown error: {e}")
