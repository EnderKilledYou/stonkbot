import unittest

from forexconnect import ForexConnect

from env import app_config
from routes.login import login

config = app_config


class LoginTest(unittest.TestCase):
    def test_login(self):
        with ForexConnect() as fx:
            fx.login(app_config["STR_USER_I_D"], app_config["STR_PASSWORD"],
                     app_config["STR_URL"],
                     app_config["STR_CONNECTION"], None, None, session_status_changed_for_test)

            print("")
            print("Accounts:")
            accounts_response_reader = fx.get_table_reader(fx.ACCOUNTS)
            count = 0
            for account in accounts_response_reader:
                print("{0:s}".format(account.account_id))
                count += 1
            self.assertGreater(count, 0)


def session_status_changed_for_test(session,
                                    status):
    pass
