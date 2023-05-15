from flask import session, redirect, request, url_for, jsonify, Blueprint, abort
from forexconnect import ForexConnect

from routes.status_changed import session_status_changed
from sharp_config import sharp_api

tables = Blueprint('tables', __name__)


@sharp_api.function()
def get_orders_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    return jsonify(get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.ORDERS))


@sharp_api.function()
def get_offers_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    return jsonify(get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.OFFERS))


@sharp_api.function()
def get_accounts_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    return jsonify(get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.ACCOUNTS))


@sharp_api.function()
def get_closed_trades_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    return jsonify(get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.CLOSED_TRADES))


@sharp_api.function()
def get_messages_trades_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    return jsonify(get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.MESSAGES))


@sharp_api.function()
def get_summary_trades_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    return jsonify(get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.SUMMARY))


@sharp_api.function()
def get_trades_table_api(str_user_i_d: str, str_password: str, str_url: str, str_connection: str):
    return jsonify(get_table(str_user_i_d, str_password, str_url, str_connection, ForexConnect.TRADES))


@sharp_api.function()
def get_price_history(str_user_i_d, str_password, str_url, str_connection):
    pass


def get_table(str_user_i_d, str_password, str_url, str_connection, table):
    with ForexConnect() as fx:
        fx.login(str_user_i_d, str_password, str_url,
                 str_connection, None, None,
                 session_status_changed)
        table_manager = fx.table_manager
        tbl = table_manager.get_table(table)
        tbl_to_list = list(map(convert_row(tbl.columns), tbl))
        return tbl_to_list


def convert_row(columns):
    def convert(row):
        item = {}
        for column in columns:
            item[column.id] = row[column.id]
        return item

    return convert
