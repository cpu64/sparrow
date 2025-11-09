import time

# mock posts for demonstration purposes
__posts = [
    {
        "text": "First post",
        "text_color": "white",
        "text_font": "Roboto",
        "created_at": "2025-10-10 10:00",
        "views": 0,
        "author": "user1",
        "tags": ["example", "demo"],
    },
    {
        "text": "Second post",
        "text_color": "white",
        "text_font": "Monoton",
        "created_at": "2025-10-11 11:00",
        "views": 0,
        "author": "user2",
        "tags": ["test"],
    },
]


def get_all_posts():
    return __posts


def get_post_by_id(post_id):
    if 0 <= post_id < len(__posts):
        return __posts[post_id]
    return None


def add_post(text, text_color, text_font, author, tags=None):
    from datetime import datetime

    new_post = {
        "text": text,
        "text_color": text_color,
        "text_font": text_font,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "views": 0,
        "author": author,
        "tags": tags if tags else [],
    }
    __posts.insert(0, new_post)
    return 0


def get_all_tags():
    tags = set()
    for post in __posts:
        tags.update(post.get("tags", []))
    return sorted(list(tags))
