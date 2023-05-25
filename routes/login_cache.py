from hashlib import md5

login_cache = {}
listeners_cache = {}


def get_user_hash(user: str, pas: str, url, connection):
    try:
        return md5(user + pas + url + connection)
    except:
        return None
