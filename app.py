import logging

from flask import Flask
from flask_cors import CORS

app = Flask(__name__, static_url_path='',
            static_folder='dist', )
CORS(app, resources={r"/api/*": {"origins": "*"}})
from routes.login import login
from routes.tables import tables





@app.route('/hello')
def hello_world():  # put application's code here
    from sharp_config.sharp_config import sharp_api
    sharp_api.generate("src/api.js")
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
