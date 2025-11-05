__galleries = [
    {
        "name": "Example gallery 1",
        "description": "This is my gallery",
        "created_at": "2025-11-01",
        "updated_at": "2025-11-05",
        "background_color": "#00aa55"
    },
    {
        "name": "Example gallery 2",
        "description": "This is my other gallery",
        "created_at": "2025-11-01",
        "updated_at": "2025-11-05",
        "background_color": "#0B92E0"
    },
]

def get_gallery():
    return __galleries[0]

def get_galleries():
    return __galleries
