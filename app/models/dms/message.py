from models.db import execute, get_one

def create_message(
    chat_id,
    sender_id,
    text
):
    msg = get_one(
        """
        INSERT INTO messages (text, seen, sender_id, chat_id)
        VALUES (%s, FALSE, %s, %s)
        RETURNING id;
        """,
        (text, sender_id, chat_id)
    )

    execute(
        """
        UPDATE chats
        SET updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'UTC'
        WHERE id = %s;
        """,
        (chat_id,)
    )

    return msg["id"]

def edit_message(
    message_id,
    text = None,
    seen = None
):
    if text is None and seen is None:
        raise ValueError("No fields to update")

    fields = []
    values = []

    if text is not None:
        fields.append("text = %s")
        values.append(text)

    if seen is not None:
        fields.append("seen = %s")
        values.append(seen)

    fields.append("updated_at = CURRENT_TIMESTAMP AT TIME ZONE 'UTC'")

    query = f"""
        UPDATE messages
        SET {', '.join(fields)}
        WHERE id = %s;
    """

    values.append(message_id)

    execute(query, tuple(values))
