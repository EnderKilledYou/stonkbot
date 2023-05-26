from hashlib import md5

login_cache = {}
listeners_cache = {}


def get_user_hash(user: str, pas: str, url, connection):
    try:
        return md5(str(user + pas + url + connection).encode('utf-8')).hexdigest()
    except Exception as e:
        return None
