from models.db import execute, get_one, get_all

def create_new_chat(name, user_a_id, user_b_id):
    row = get_one("""
        WITH new_chat AS (
            INSERT INTO chats (name)
            VALUES (%s)
            RETURNING id
        ),
        members AS (
            INSERT INTO chat_members (member_id, chat_id)
            SELECT %s, id FROM new_chat
            UNION ALL
            SELECT %s, id FROM new_chat
        )
        SELECT id FROM new_chat;
    """, (name, user_a_id, user_b_id))

    return row["id"]

def leave_chat(chat_id, user_id):
    execute(
        """
        DELETE FROM chat_members
        WHERE chat_id = %s AND member_id = %s;
        """,
        (chat_id, user_id)
    )

    remaining = get_one(
        """
        SELECT COUNT(*) AS count
        FROM chat_members
        WHERE chat_id = %s;
        """,
        (chat_id,)
    )["count"]

    if remaining == 0:
        execute(
            """
            DELETE FROM chats
            WHERE id = %s;
            """,
            (chat_id,)
        )

def get_chats_with_unseen_messages(user_id):
    return get_all(
        """
        SELECT
            c.id AS chat_id,
            c.name,
            c.updated_at,
            COUNT(m.id) AS unseen_count
        FROM chats c
        JOIN chat_members cm
            ON cm.chat_id = c.id
        JOIN messages m
            ON m.chat_id = c.id
        WHERE
            cm.member_id = %s
            AND m.seen = FALSE
            AND m.sender_id != %s
        GROUP BY
            c.id, c.name, c.updated_at
        ORDER BY
            c.updated_at DESC;
        """,
        (user_id, user_id)
    )

def get_all_users():
    return get_all("SELECT id, email FROM users ORDER BY id;")

def mark_chat_messages_as_seen(chat_id, user_id):
    try:
        result = get_one(
            """
            UPDATE messages
            SET
                seen = TRUE,
                updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'UTC'
            WHERE
                chat_id = %s
                AND sender_id != %s
                AND seen = FALSE;
            """,
            (chat_id, user_id)
        )
    except:
        print("likely no messages to mark as seen, failing silently")

def get_messages_for_chat(chat_id):
    return get_all(
        """
        SELECT
            id,
            text,
            seen,
            created_at,
            updated_at,
            sender_id,
            chat_id
        FROM messages
        WHERE chat_id = %s
        ORDER BY created_at ASC;
        """,
        (chat_id,)
    )

def list_chats_for_user(user_id):
    return get_all(
        """
        SELECT
            c.id AS chat_id,
            c.name
        FROM chats c
        JOIN chat_members cm
            ON cm.chat_id = c.id
        WHERE cm.member_id = %s
        ORDER BY c.updated_at DESC;
        """,
        (user_id,)
    )

def get_chat_name(chat_id):
    chat = get_one(
        """
        SELECT name
        FROM chats
        WHERE id = %s;
        """,
        (chat_id,)
    )

    return chat["name"] if chat else ""
