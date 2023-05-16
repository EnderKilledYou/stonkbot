from flask import jsonify, Blueprint
from forexconnect import ForexConnect

from routes.status_changed import session_status_changed

login = Blueprint('login', __name__)
from sharp_config.sharp_config import sharp_api


@sharp_api.function()
def login(str_user_i_d: str, str_password: str, str_url: str, str_connection: str, str_session_id: str, str_pin: str):
    with ForexConnect() as fx:
        try:
            fx.login(str_user_i_d, str_password, str_url,
                     str_connection, None, None,
                     session_status_changed)
            return {'authenticated': True}
        except Exception as e:
            print(e)
        return {'authenticated': False}
