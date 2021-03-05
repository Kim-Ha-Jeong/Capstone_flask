import os
from pathlib import Path

import flask
import io
from flask import send_file
from flask_login import LoginManager, login_user, current_user, logout_user

from src.fulls import *
from src.users import *
from src.edits import *
from src.login import *

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['JSON_AS_ASCII'] = False
login_manager = LoginManager()
login_manager.init_app(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, 'input/')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'output/')

@login_manager.user_loader
def load_user(user_id):
    return USERS[user_id]


@app.route('/')
def show_url():
    return render_template('url.html')


# input 비디오 src
@app.route("/input/<fileName>", methods=["GET"])
def full(fileName):
    path = INPUT_FOLDER + fileName

    if os.path.isfile(path):
        return send_file(path, mimetype='multipart/form')
    else:
        return 'error'


# output 비디오 src
@app.route("/output/<fileName>", methods=["GET"])
def edited(fileName):
        path = OUTPUT_FOLDER + fileName
        if os.path.isfile(path):
            return send_file(path, mimetype='multipart/form')
        else:
            return 'error'


# full, edited 비디오 보여주는 화면
@app.route("/video/<fileName>", methods=["GET"])
def show_video(fileName):
    output_path = OUTPUT_FOLDER + fileName
    input_path = INPUT_FOLDER + fileName
    if os.path.isfile(output_path):
        return render_template('video.html', data=fileName, folder='output')
    elif os.path.isfile(input_path):
        return render_template('video.html', data=fileName, folder='input')
    else:
        return 'error'


app.register_blueprint(user_api, url_prefix='/api')
app.register_blueprint(full_api, url_prefix='/api')
app.register_blueprint(edit_api, url_prefix='/api')
app.register_blueprint(login_api)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port='5001',debug=True, threaded=True)
