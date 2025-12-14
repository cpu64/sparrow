from models.db import get_one, get_all, execute
import psycopg2

POST_COLUMN_LENGTHS = {"content": [1, 500], "text_color": [7, 7]}


def check_length(key, value):
    if POST_COLUMN_LENGTHS[key][0] <= len(value) <= POST_COLUMN_LENGTHS[key][1]:
        return False
    return f"{POST_COLUMN_LENGTHS[key][0]} and {POST_COLUMN_LENGTHS[key][1]}"


def get_post(post_id):
    try:
        post = get_one(
            """
            SELECT p.id, p.content, p.text_color, p.text_font, p.created_at, p.views,
                   u.username AS username,
                   COALESCE(a.url, 'https://avatar.iran.liara.run/public/6') AS author_avatar
            FROM posts p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN avatars a ON u.avatar_id = a.id
            WHERE p.id = %s
        """,
            (post_id,),
        )
        if post:
            return post
        return "No such post."
    except Exception as e:
        print(f"Error occurred while fetching post data: {e}")
        return "Error occurred while fetching post data."


def increase_views(post_id):
    try:
        execute(
            """
            UPDATE posts
            SET views = views + 1
            WHERE id = %s;
        """,
            (post_id,),
        )
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."


def get_posts(tags=[], limit=10, last_retrieved=None):
    try:
        params = []
        if tags:
            query = """
                SELECT p.id, p.content, p.text_color, p.text_font, p.created_at, p.views,
                       u.username, COALESCE(a.url, 'https://avatar.iran.liara.run/public/6') AS author_avatar
                FROM posts p
                JOIN users u ON p.user_id = u.id
                LEFT JOIN avatars a ON u.avatar_id = a.id
                JOIN post_tags pt ON p.id = pt.post_id
                JOIN tags t ON pt.tag_id = t.id
                WHERE t.name = ANY(%s)
            """
            params.append(tags)
            if last_retrieved:
                query += " AND p.created_at < %s"
                params.append(last_retrieved)
            query += """
                GROUP BY p.id, u.username, a.url
                HAVING COUNT(DISTINCT t.name) = %s
                ORDER BY p.created_at DESC
                LIMIT %s
            """
            params.append(len(tags))
            params.append(limit)
        else:
            query = """
                SELECT p.id, p.content, p.text_color, p.text_font, p.created_at, p.views,
                       u.username, COALESCE(a.url, 'https://avatar.iran.liara.run/public/6') AS author_avatar
                FROM posts p
                JOIN users u ON p.user_id = u.id
                LEFT JOIN avatars a ON u.avatar_id = a.id
            """
            if last_retrieved:
                query += " WHERE p.created_at < %s"
                params.append(last_retrieved)
            query += """
                ORDER BY p.created_at DESC
                LIMIT %s
            """
            params.append(limit)
        posts = get_all(query, tuple(params))
        if posts:
            return posts
        return []
    except Exception as e:
        print(f"Error occurred while fetching posts data: {e}")
        return "Error occurred while fetching posts data."


def add_post(user_id, content, text_color, text_font, tags=[]):
    try:
        ret = get_one(
            """
            INSERT INTO posts (user_id, content, text_color, text_font)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """,
            (user_id, content, text_color, text_font),
            commit=True,
        )
        post_id = ret["id"]
        for tag in tags:
            execute(
                """
                INSERT INTO post_tags (post_id, tag_id)
                VALUES (%s, (SELECT id FROM tags WHERE name = %s))
            """,
                (post_id, tag),
            )
        return post_id
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."


def remove_post(post_id):
    try:
        execute(
            """
            DELETE FROM posts WHERE id = %s
        """,
            (post_id,),
        )
    except Exception as e:
        print(f"Unknown error: {e}")
        return "Unknown error."


def get_text_fonts():
    try:
        fonts = get_all("""SELECT id, name FROM text_fonts ORDER BY id DESC""")
        if fonts:
            return fonts
        return []
    except Exception as e:
        print(f"Error occurred while fetching font data: {e}")
        return "Error occurred while fetching font data."
