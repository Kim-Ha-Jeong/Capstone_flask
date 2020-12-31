from flask_restful import Api
from flask import Flask, send_file

from fulls import *
from users import *

app = Flask(__name__)


app.register_blueprint(user_api, url_prefix='/api')
app.register_blueprint(full_api, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)
