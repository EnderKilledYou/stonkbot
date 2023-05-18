from flask import Blueprint
from forexconnect import ForexConnect

from routes.login_cache import login_cache
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
        if str_user_i_d in login_cache:
            with login_cache[str_user_i_d]:
                pass
        login_cache[str_user_i_d] = fx
        return {'authenticated': True}
    except Exception as e:
        print(e)
    return {'authenticated': False}
