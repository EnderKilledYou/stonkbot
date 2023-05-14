import os

from dotenv import dotenv_values

app_config = {
    **dotenv_values(".env"),  # load production env
    **dotenv_values(".env.local"),  # load dev env
    **os.environ,  # override loaded values with environment variables
}
