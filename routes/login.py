from flask import jsonify, Blueprint
from forexconnect import ForexConnect

from routes.status_changed import session_status_changed
from sharp_config import sharp_api

login = Blueprint('login', __name__)


@sharp_api.function()
def login(str_user_i_d: str, str_password: str, str_url: str, str_connection: str, str_session_id: str, str_pin: str):
    with ForexConnect() as fx:
        try:
            fx.login(str_user_i_d, str_password, str_url,
                     str_connection, None, None,
                     session_status_changed)

            print("")
            print("Accounts:")
            accounts_response_reader = fx.get_table_reader(fx.ACCOUNTS)
            for account in accounts_response_reader:
                print("{0:s}".format(account.account_id))

            print("")
        except Exception as e:
            print(e)
        try:
            fx.logout()
        except Exception as e:
            print(e)
    return jsonify({})


