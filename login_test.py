import unittest

from env import app_config
from routes.login import login


class LoginTest(unittest.TestCase):
    def test_login(self):

        config = app_config
        login(app_config["STR_USER_I_D"],app_config["STR_PASSWORD"],app_config["STR_URL"],app_config["STR_CONNECTION"],app_config["STR_SESSION_ID"],app_config["STR_PIN"])
        pass
