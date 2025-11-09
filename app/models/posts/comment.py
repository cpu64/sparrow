import datetime

# mock comments for demonstration purposes
__comments = [
    {
        "text": "Great post!",
        "author": "admin",
        "created_at": "2025-10-10 12:00",
        "post_id": 0,
    },
    {
        "text": "Thanks for sharing.",
        "author": "admin",
        "created_at": "2025-10-11 13:00",
        "post_id": 0,
    },
]


def get_comments_by_post_id(post_id):
    return [comment for comment in __comments if comment["post_id"] == post_id]


def add_comment(text, author, post_id):
    new_comment = {
        "text": text,
        "author": author,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "post_id": post_id,
    }
    __comments.append(new_comment)


def delete_comment_by_id(comment_id):
    if 0 <= comment_id < len(__comments):
        del __comments[comment_id]
