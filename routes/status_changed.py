from forexconnect import ForexConnect


def session_status_changed(session,
                           status):
    pass


def get_account(table_manager):
    accounts_table = table_manager.get_table(ForexConnect.ACCOUNTS)
    for account_row in accounts_table:
        print("AccountID: {0:s}, Balance: {1:.5f}".format(account_row.account_id, account_row.balance))
    return accounts_table.get_row(0)
