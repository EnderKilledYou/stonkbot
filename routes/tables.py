import time

from flask import jsonify, Blueprint
from forexconnect import ForexConnect, fxcorepy

from routes.login_cache import login_cache
from routes.status_changed import session_status_changed

tables = Blueprint('tables', __name__)
from sharp_config.sharp_config import sharp_api


@sharp_api.function()
def sell_order(str_instr: str, amount: int, str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    if str_user_i_d in login_cache:
        fx = login_cache[str_user_i_d]
        offer = get_offer(fx, str_instr)
        account = get_account(fx)
        trade = Common.get_trade(fx, str_account, offer.offer_id)

        if not trade:
            raise Exception("There are no opened positions for instrument '{0}'".format(instrument))

        if not account:
            raise Exception(
                "The account '{0}' is not valid".format(account))
        else:
            str_account = account.account_id
            print("AccountID='{0}'".format(str_account))
        request = fx.create_order_request(
            order_type=fxcorepy.Constants.Orders.TRUE_MARKET_CLOSE,
            OFFER_ID=offer.offer_id,
            ACCOUNT_ID=str_account,
            BUY_SELL=fxcorepy.Constants.SELL,
            AMOUNT=amount,
            TRADE_ID=trade.trade_id
        )

        if request is None:
            raise Exception("Cannot create request")


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


price_columns = ['Time', 'Price' ]


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


def get_offer(fx, s_instrument):
    table_manager = fx.table_manager
    offers_table = table_manager.get_table(ForexConnect.OFFERS)
    for offer_row in offers_table:
        if offer_row.instrument == s_instrument:
            return offer_row


def get_account(table_manager):
    accounts_table = table_manager.get_table(ForexConnect.ACCOUNTS)
    return accounts_table.get_row(0)
