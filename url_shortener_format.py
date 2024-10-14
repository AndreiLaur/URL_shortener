import hashlib


def get_short_url(long_url: str):
    hashed_url = hashlib.sha256(long_url.encode())
    short_hash = hashed_url.hexdigest()[:8]
    return f"short_url.com/{short_hash}"
