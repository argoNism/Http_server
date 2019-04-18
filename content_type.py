CONTENT_TYPE_MAP = {
    "html": "text/html",
    "css": "text/css",
    "js": "text/javascript",
    "txt": "text/plane",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "ico": "image/vnd.microsoft.icon"
}

def get_content_text(ext: str) -> str:
    if ext in CONTENT_TYPE_MAP:
        return CONTENT_TYPE_MAP[ext]
    elif ext.lower() in CONTENT_TYPE_MAP:
        return  CONTENT_TYPE_MAP[ext.lower()]
    else:
        return "application/octet-stream"