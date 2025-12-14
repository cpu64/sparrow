# models/db.py
import psycopg2
import os
import sys


db_params = {
    "dbname": os.getenv("PGDATABASE", "sparrow"),
    "user": os.getenv("PGUSER", "sparrow"),
    "password": os.getenv("PGPASSWORD", "overwriteme"),
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", 5432),
}


def get_db_connection():
    return psycopg2.connect(**db_params)


def execute(query, values=()):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        result = cur.fetchone() if cur.description else None
        conn.commit()
        return result[0] if result else None

    except Exception as e:
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_one(query, values=(), commit=False):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        if commit:
            conn.commit()
        data = cur.fetchone()
        conn.commit()

        if data:
            columns = [desc[0] for desc in cur.description]
            data_dict = dict(zip(columns, data))
            return data_dict
        return None
    except Exception as e:
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_all(query, values=()):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        data = cur.fetchall()
        conn.commit()

        if data:
            columns = [desc[0] for desc in cur.description]
            data_dict = [dict(zip(columns, i)) for i in data]
            return data_dict
        return []

    except Exception as e:
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def init_db():
    conn = None
    cur = None
    try:
        from .users.avatar import AVATAR_COLUMN_LENGTHS
        from .users.user import USER_COLUMN_LENGTHS
        from .posts.post import POST_COLUMN_LENGTHS
        from .posts.comment import COMMENT_COLUMN_LENGTHS as POST_COMMENT_COLUMN_LENGTHS
        from .posts.tag import TAG_COLUMN_LENGTHS
        from .gallery.gallery import GALLERY_COLUMN_LENGTHS
        from .gallery.image import IMAGE_COLUMN_LENGTHS
        from .gallery.image_comment import COMMENT_COLUMN_LENGTHS

        conn = get_db_connection()
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            """
        CREATE SCHEMA IF NOT EXISTS sparrow;
        SET search_path TO sparrow;
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS avatars (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(%(name_length)s) UNIQUE NOT NULL,
            url TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
        );
        """,
            {"name_length": AVATAR_COLUMN_LENGTHS["name"][1]},
        )

        cur.execute(
            """
        INSERT INTO avatars (name, url)
        VALUES ('Default Sparrow', 'https://github.githubassets.com/assets/pull-shark-default-498c279a747d.png')
        ON CONFLICT (name) DO NOTHING;"""
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS users (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            username VARCHAR(%(username_length)s) UNIQUE NOT NULL,
            password VARCHAR(%(password_length)s) NOT NULL,
            twofa_secret VARCHAR(%(twofa_secret_length)s),
            name VARCHAR(%(name_length)s),
            surname VARCHAR(%(surname_length)s),
            email VARCHAR(%(email_length)s),
            description VARCHAR(%(description_length)s),
            date_of_birth DATE,
            phone_number VARCHAR(%(phone_number_length)s),
            pronouns VARCHAR(%(pronouns_length)s),
            sex BOOLEAN,
            gender VARCHAR(%(gender_length)s),
            country VARCHAR(%(country_length)s),
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            updated_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            last_login TIMESTAMP,
            last_login_attempt TIMESTAMP,
            banned BOOLEAN NOT NULL DEFAULT FALSE,
            admin BOOLEAN NOT NULL DEFAULT FALSE,
            avatar_id INT NOT NULL DEFAULT 1 REFERENCES avatars(id)
        );
        """,
            {
                "username_length": USER_COLUMN_LENGTHS["username"][1],
                "password_length": USER_COLUMN_LENGTHS["password"][1],
                "twofa_secret_length": USER_COLUMN_LENGTHS["twofa_secret"][1],
                "name_length": USER_COLUMN_LENGTHS["name"][1],
                "surname_length": USER_COLUMN_LENGTHS["surname"][1],
                "email_length": USER_COLUMN_LENGTHS["email"][1],
                "description_length": USER_COLUMN_LENGTHS["description"][1],
                "phone_number_length": USER_COLUMN_LENGTHS["phone_number"][1],
                "pronouns_length": USER_COLUMN_LENGTHS["pronouns"][1],
                "gender_length": USER_COLUMN_LENGTHS["gender"][1],
                "country_length": USER_COLUMN_LENGTHS["country"][1],
            },
        )

        # -- post substystem --
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS posts (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            content VARCHAR(%(content_length)s) NOT NULL,
            text_color VARCHAR(%(text_color_length)s) NOT NULL DEFAULT '#ffffff',
            text_font INT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2'),
            views INT NOT NULL DEFAULT 0,
            user_id INT NOT NULL REFERENCES users(id)
        );
        """,
            {
                "content_length": POST_COLUMN_LENGTHS["content"][1],
                "text_color_length": POST_COLUMN_LENGTHS["text_color"][1],
            },
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS comments (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            content VARCHAR(%(content_length)s) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2'),
            user_id INT  NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            post_id INT NOT NULL REFERENCES posts(id) ON DELETE CASCADE
        );
        """,
            {
                "content_length": POST_COMMENT_COLUMN_LENGTHS["content"][1],
            },
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS tags (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(%(name_length)s) UNIQUE NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC+2')
        );
        """,
            {
                "name_length": TAG_COLUMN_LENGTHS["name"][1],
            },
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS post_tags (
            post_id INT REFERENCES posts(id) ON DELETE CASCADE,
            tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
            PRIMARY KEY (post_id, tag_id)
        );
        """
        )
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS text_fonts(
        id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
        );"""
        )

        cur.execute(
            """
        INSERT INTO text_fonts (name)
        VALUES
        ('Roboto'),
        ('Pacifico'),
        ('Monoton')
        ON CONFLICT (name) DO NOTHING;
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS chats (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(60) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            updated_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
        );
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS messages (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            text VARCHAR(255) NOT NULL,
            seen BOOLEAN NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            updated_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            sender_id INT NOT NULL,
            chat_id INT NOT NULL,
            CONSTRAINT fk_sender_id FOREIGN KEY (sender_id) references users(id) ON DELETE CASCADE,
            CONSTRAINT fk_chat_id FOREIGN KEY (chat_id) references chats(id) ON DELETE CASCADE
        );
        """
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS chat_members (
            member_id INT NOT NULL,
            chat_id INT NOT NULL,
            CONSTRAINT fk_member_id FOREIGN KEY (member_id) references users(id),
            CONSTRAINT fk_chat_id FOREIGN KEY (chat_id) references chats(id)
        );
        """
        )
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS galleries (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(%(name_length)s) NOT NULL,
            description VARCHAR(%(description_length)s),
            background_color VARCHAR(%(background_color_length)s),
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            updated_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE
        );
        """,
            {
                "name_length": GALLERY_COLUMN_LENGTHS["name"][1],
                "description_length": GALLERY_COLUMN_LENGTHS["description"][1],
                "background_color_length": GALLERY_COLUMN_LENGTHS["background_color"][
                    1
                ],
            },
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS images (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name VARCHAR(%(name_length)s) NOT NULL,
            url VARCHAR(%(url_length)s) NOT NULL,
            description VARCHAR(%(description_length)s),
            location VARCHAR(%(location_length)s),
            taken_at DATE,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            gallery_id INT NOT NULL REFERENCES galleries(id) ON DELETE CASCADE
        );
        """,
            {
                "name_length": IMAGE_COLUMN_LENGTHS["name"][1],
                "url_length": IMAGE_COLUMN_LENGTHS["url"][1],
                "description_length": IMAGE_COLUMN_LENGTHS["description"][1],
                "location_length": IMAGE_COLUMN_LENGTHS["location"][1],
            },
        )

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS image_comments (
            id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            text VARCHAR(%(text_length)s) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
            user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            image_id INT NOT NULL REFERENCES images(id) ON DELETE CASCADE
        );
        """,
            {"text_length": COMMENT_COLUMN_LENGTHS["text"][1]},
        )

        print("Database initialized successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
        if conn:
            conn.close()
        sys.exit(1)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
