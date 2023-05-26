from flask import Blueprint
from forexconnect import ForexConnect

from routes.login_cache import login_cache, listeners_cache, get_user_hash
from routes.status_changed import session_status_changed

login = Blueprint('login', __name__)
from sharp_config.sharp_config import sharp_api


@sharp_api.function()
def login(str_user_i_d: str, str_password: str, str_url: str, str_connection: str, str_session_id: str, str_pin: str):
    try:
        fx = ForexConnect()
        fx.login(str_user_i_d, str_password, str_url,
                 str_connection, None, None,
                 session_status_changed)
        user_hash = get_user_hash(str_user_i_d, str_password, str_url, str_connection)
        if user_hash is None:
            return {'message': 'invalid sequence'}
        if str_user_i_d in listeners_cache:
            for listener in listeners_cache[user_hash]:
                listener.unsubscribe()
            listeners_cache[user_hash].clear()
        else:
            listeners_cache[user_hash] = []

        if user_hash in login_cache:
            with login_cache[user_hash]:
                pass

        login_cache[user_hash] = fx
        return {'authenticated': True, 'user_hash': user_hash}
    except Exception as e:
        print(e)
        return {'error': str(e)}
    return {'authenticated': False,'message': 'could not log you in'}
