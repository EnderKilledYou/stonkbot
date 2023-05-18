import time

from flask import jsonify, Blueprint
from forexconnect import ForexConnect

from routes.login_cache import login_cache
from routes.status_changed import session_status_changed

tables = Blueprint('tables', __name__)
from sharp_config.sharp_config import sharp_api


@sharp_api.function()
def get_orders_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    """

        :param str_user_i_d: The User login
        :param str_password: The User Password
        :param str_url: The url of the F-Service
        :param str_connection: Demo or live
        :return: Json list of the orders table
        """
    return get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.ORDERS)


@sharp_api.function()
def get_offers_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    """

        :param str_user_i_d: The User login
        :param str_password: The User Password
        :param str_url: The url of the F-Service
        :param str_connection: Demo or live
        :return: Json list of the offers table
        """
    return get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.OFFERS)


@sharp_api.function()
def get_accounts_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    """

        :param str_user_i_d: The User login
        :param str_password: The User Password
        :param str_url: The url of the F-Service
        :param str_connection: Demo or live
        :return: Json list of the accounts table
        """
    return get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.ACCOUNTS)


@sharp_api.function()
def get_closed_trades_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    """

        :param str_user_i_d: The User login
        :param str_password: The User Password
        :param str_url: The url of the F-Service
        :param str_connection: Demo or live
        :return: Json list of the trades table
        """
    return get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.CLOSED_TRADES)


@sharp_api.function()
def get_messages_trades_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    """

        :param str_user_i_d: The User login
        :param str_password: The User Password
        :param str_url: The url of the F-Service
        :param str_connection: Demo or live
        :return: Json list of the trades table
        """
    return get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.MESSAGES)


@sharp_api.function()
def get_summary_trades_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    """

        :param str_user_i_d: The User login
        :param str_password: The User Password
        :param str_url: The url of the F-Service
        :param str_connection: Demo or live
        :return: Json list of the trades table
        """
    return get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.SUMMARY)


@sharp_api.function()
def get_trades_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    """

    :param str_user_i_d: The User login
    :param str_password: The User Password
    :param str_url: The url of the F-Service
    :param str_connection: Demo or live
    :return: Json list of the trades table
    """
    return get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.TRADES)


price_columns = ['Time', 'Price 1', 'Price 2', 'Price 3', 'Price 4', 'Price 5', 'Price 6', 'Price 7',
                 'Price 8', '---']


@sharp_api.function()
def get_price_history(str_instr: str, str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    try:
        if str_user_i_d in login_cache:
            fx = login_cache[str_user_i_d]
            history = fx.get_history(str_instr, "m1", None, None, 20)
            output = history.tolist()
            for i in range(0, len(output)):
                item = output[i]
                s = int(item[0] / 1000000000)
                rme = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s))
                output[i] = {}

                tmp = [rme] + list(item[1:])
                for j in range(0, len(price_columns)):
                    output[i][price_columns[j]] = tmp[j]

            return {'columns': price_columns, 'tbl': output}
            tbl_to_list = list(map(convert_row(history.columns), history))
            columns_to_list = list(map(lambda x: x.id, history.columns))
            return {'columns': columns_to_list, 'tbl': tbl_to_list}
    except Exception as e:
        return {'error': str(e)}


def get_table(str_user_i_d, str_password, str_url, str_connection, table):
    """

    :param str_user_i_d: The User login
    :param str_password: The User Password
    :param str_url: The url of the F-Service
    :param str_connection: Demo or live
    :param table: The table you want
    :return:
    """
    if str_user_i_d in login_cache:
        fx = login_cache[str_user_i_d]
        fx.login(str_user_i_d, str_password, str_url,
                 str_connection, None, None,
                 session_status_changed)
        table_manager = fx.table_manager
        tbl = table_manager.get_table(table)
        tbl_to_list = list(map(convert_row(tbl.columns), tbl))
        columns_to_list = list(map(lambda x: x.id, tbl.columns))
        return {'columns': columns_to_list, 'tbl': tbl_to_list}


def convert_row(columns):
    def convert(row):
        item = {}
        for column in columns:
            item[column.id] = row[column.id]
        return item

    return convert
