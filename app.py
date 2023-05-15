from flask import Flask
from sharp import Sharp, naming

app = Flask(__name__)


from routes.login import login
from routes.tables import tables

@app.route('/')
def hello_world():  # put application's code here
    from sharp_config.sharp_config import sharp_api
    sharp_api.generate("src/api.js")
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
