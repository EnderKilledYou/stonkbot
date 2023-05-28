import time

from flask import Blueprint
from forexconnect import ForexConnect, fxcorepy, Common

from routes.login_cache import login_cache, listeners_cache

tables = Blueprint('tables', __name__)
from sharp_config.sharp_config import sharp_api


@sharp_api.function()
def sell_order(str_instr: str, amount: int, rate: float, order_type: str, user_hash: str):
    if user_hash is None:
        return {'message': 'invalid sequence'}
    if user_hash not in login_cache:
        return {'message': "Relogin"}

    fx = login_cache[user_hash]
    account = Common.get_account(fx)

    if not account:
        return {'message': "No Such Account"}

    offer = Common.get_offer(fx, str_instr)
    if not offer:
        return {'message': "No Such Offer"}

    order = get_order_type(order_type)
    if not order:
        return {'message': "No Such Order Type"}

    str_account = account.account_id
    trade = Common.get_trade(fx, str_account, offer.offer_id)

    if not trade:
        return {'message': "There are no trades for instrument '{0}'".format(str_instr)}

    try:
        request = fx.create_order_request(
            order_type=order,
            SYMBOL=offer.instrument,
            ACCOUNT_ID=str_account,
            BUY_SELL=fxcorepy.Constants.SELL,
            AMOUNT=amount,
            RATE=rate,
            TRADE_ID=trade.trade_id
        )
        if request is not None:
            resp = fx.send_request(request)
            order_id = resp.order_id
            return {'success': True, 'message': "Order is " + order_id}
    except Exception as e:
        return {'message': str(e)}

    return {'message': "The exchange doesn't Do This"}


def get_order_type(order_type):
    if order_type == "LIMIT":
        return fxcorepy.Constants.Orders.LIMIT
    if order_type == "LIMIT_ENTRY":
        return fxcorepy.Constants.Orders.LIMIT_ENTRY
    if order_type == "MARKET_CLOSE":
        return fxcorepy.Constants.Orders.MARKET_CLOSE
    if order_type == "MARKET_CLOSE_RANGE":
        return fxcorepy.Constants.Orders.MARKET_CLOSE_RANGE
    if order_type == "OPEN_LIMIT":
        return fxcorepy.Constants.Orders.OPEN_LIMIT
    if order_type == "STOP":
        return fxcorepy.Constants.Orders.STOP
    if order_type == "STOP_ENTRY":
        return fxcorepy.Constants.Orders.STOP_ENTRY
    if order_type == "TRUE_MARKET_CLOSE":
        return fxcorepy.Constants.Orders.TRUE_MARKET_CLOSE
    if order_type == "TRUE_MARKET_OPEN":
        return fxcorepy.Constants.Orders.TRUE_MARKET_OPEN
    if order_type == "ENTRY":
        return fxcorepy.Constants.Orders.ENTRY
    if order_type == "CLOSE_ENTRY":
        return fxcorepy.Constants.Orders.CLOSE_ENTRY
    if order_type == "STOP_ENTRY":
        return fxcorepy.Constants.Orders.STOP_ENTRY


@sharp_api.function()
def buy_market(str_instr: str, amount: int, user_hash: str):
    if user_hash is None:
        return {'message': 'invalid sequence'}
    if user_hash not in login_cache:
        return {'message': "Relogin"}

    fx = login_cache[user_hash]
    account = Common.get_account(fx)

    if not account:
        return {'message': "No Such Account"}

    offer = Common.get_offer(fx, str_instr)
    if not offer:
        return {'message': "No Such Offer"}

    order = fxcorepy.Constants.Orders.CLOSE_ENTRY

    str_account = account.account_id

    try:
        request = fx.create_order_request(
            order_type=order,
            SYMBOL=offer.instrument,
            ACCOUNT_ID=str_account,
            BUY_SELL=fxcorepy.Constants.BUY,
            AMOUNT=amount,

        )
        if request is not None:
            resp = fx.send_request(request)
            order_id = resp.order_id
            return {'success': True, 'message': "Order is " + order_id}
    except Exception as e:
        return {'message': str(e)}

    return {'message': "The exchange doesn't Do This"}


@sharp_api.function()
def close_trade(str_instr: str, amount: int, trade_id: int, user_hash: str):
    if user_hash is None:
        return {'message': 'invalid sequence'}
    if user_hash not in login_cache:
        return {'message': "Relogin"}

    fx = login_cache[user_hash]
    account = Common.get_account(fx)

    if not account:
        return {'message': "No Such Account"}

    offer = Common.get_offer(fx, str_instr)
    if not offer:
        return {'message': "No Such Offer"}

    order = fxcorepy.Constants.Orders.MARKET_CLOSE

    str_account = account.account_id

    try:
        bid = offer.bid
        request = fx.create_order_request(
            order_type=order,
            AMOUNT=amount,
            OFFER_ID=offer.offer_id,
            ACCOUNT_ID=str_account,
            BUY_SELL=fxcorepy.Constants.SELL,
            TRADE_ID=trade_id,
            RATE=bid
        )
        if request is not None:
            resp = fx.send_request(request)
            order_id = resp.order_id
            return {'success': True, 'message': "Order is " + order_id}
    except Exception as e:
        return {'message': str(e)}

    return {'message': "The exchange doesn't Do This"}


@sharp_api.function()
def sell_market(str_instr: str, amount: int, user_hash: str):
    if user_hash is None:
        return {'message': 'invalid sequence'}
    if user_hash not in login_cache:
        return {'message': "Relogin"}

    fx = login_cache[user_hash]
    account = Common.get_account(fx)

    if not account:
        return {'message': "No Such Account"}

    offer = Common.get_offer(fx, str_instr)
    if not offer:
        return {'message': "No Such Offer"}

    order = fxcorepy.Constants.Orders.TRUE_MARKET_CLOSE

    str_account = account.account_id
    trade = Common.get_trade(fx, str_account, offer.offer_id)

    if not trade:
        return {'message': "There are no trades for instrument '{0}'".format(str_instr)}
    try:
        request = fx.create_order_request(
            order_type=order,
            SYMBOL=offer.instrument,
            ACCOUNT_ID=str_account,
            BUY_SELL=fxcorepy.Constants.SELL,
            AMOUNT=amount,
            TRADE_ID=trade.trade_id
        )
        if request is not None:
            resp = fx.send_request(request)
            order_id = resp.order_id
            return {'success': True, 'message': "Order is " + order_id}
    except Exception as e:
        return {'message': str(e)}

    return {'message': "The exchange doesn't Do This"}


@sharp_api.function()
def buy_order(str_instr: str, amount: int, rate: float, order_type: str, user_hash: str):
    if user_hash is None:
        return {'message': 'invalid sequence'}
    if user_hash not in login_cache:
        return {'message': "Relogin"}

    fx = login_cache[user_hash]
    account = Common.get_account(fx)

    if not account:
        return {'message': "No Such Account"}

    offer = Common.get_offer(fx, str_instr)
    if not offer:
        return {'message': "No Such Offer"}

    order = get_order_type(order_type)
    if not order:
        return {'message': "No Such Order Type"}

    str_account = account.account_id

    try:
        request = fx.create_order_request(
            order_type=order,
            SYMBOL=offer.instrument,
            ACCOUNT_ID=str_account,
            BUY_SELL=fxcorepy.Constants.BUY,
            AMOUNT=amount,
            RATE=rate,

        )
        if request is not None:
            resp = fx.send_request(request)
            order_id = resp.order_id
            return {'success': True, 'message': "Order is " + order_id}
    except Exception as e:
        return {'message': str(e)}

    return {'message': "The exchange doesn't Do This"}


@sharp_api.function()
def get_orders_table_api(user_hash: str):
    """

        :param user_hash: The User hash

        :return: Json list of the orders table
        """
    return get_table(user_hash, ForexConnect.ORDERS)


@sharp_api.function()
def get_offers_table_api(user_hash: str):
    """

        :param user_hash: The User hash

        :return: Json list of the offers table
        """
    return get_table(user_hash, ForexConnect.OFFERS)


@sharp_api.function()
def get_accounts_table_api(user_hash: str):
    """

        :param user_hash: The User hash

        :return:   list of the accounts table
        """
    return get_table(user_hash, ForexConnect.ACCOUNTS)


@sharp_api.function()
def get_closed_trades_table_api(user_hash: str):
    """

        :param user_hash: The User hash

        :return:   list of the trades table
        """
    return get_table(user_hash, ForexConnect.CLOSED_TRADES)


@sharp_api.function()
def get_messages_trades_table_api(user_hash: str):
    """

        :param user_hash: The User hash

        :return:   list of the trades table
        """
    return get_table(user_hash, ForexConnect.MESSAGES)


@sharp_api.function()
def get_summary_trades_table_api(user_hash: str):
    """

        :param user_hash: The User hash

        :return:   list of the trades table
        """
    return get_table(user_hash, ForexConnect.SUMMARY)


@sharp_api.function()
def get_trades_table_api(user_hash: str):
    """

    :param user_hash: The User hash

    :return: Json list of the trades table
    """
    return get_table(user_hash, ForexConnect.TRADES)


price_columns = ['Time', 'bid_open', 'bid_high', 'bid_low', 'bid_close', 'ask_open', 'ask_high', 'ask_low', 'ask_close',
                 'volume']


@sharp_api.function()
def get_price_history(str_instr: str, user_hash: str):
    try:

        if user_hash is None:
            return {'message': 'invalid sequence'}
        if user_hash not in login_cache:
            return {'message': "Relogin"}
        fx = login_cache[user_hash]
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

    except Exception as e:
        return {'message': str(e)}


listeners = {}


def on_added(table_listener, row_id, row):
    return


def on_changed(table_listener, row_id, row):
    return


def on_deleted(table_listener, row_id, row):
    return


def on_status_changed(table_listener, status):
    return


def get_table(user_hash: str, table):
    """

    :param user_hash: The User hash

    :param table: The table you want
    :return:
    """

    if user_hash is None:
        return {'message': 'invalid sequence'}
    if user_hash not in login_cache:
        return {'message': "Relogin"}

    fx = login_cache[user_hash]

    table_manager = fx.table_manager

    tbl = table_manager.get_table(table)

    table_name = user_hash + str(table)
    if table_name not in listeners:
        listeners[table_name] = Common.subscribe_table_updates(tbl,
                                                               on_change_callback=on_changed,
                                                               on_add_callback=on_added,
                                                               on_delete_callback=on_deleted,
                                                               on_status_change_callback=on_changed
                                                               )
        listeners_cache[user_hash].append(listeners[table_name])

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
