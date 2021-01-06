from flask import send_file

from src.fulls import *
from src.users import *
from src.login import *
from src.edits import *

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['JSON_AS_ASCII'] = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads/')


@app.route('/')
def show_url():
    return render_template('url.html')


@app.route("/video/<fileName>", methods=["GET"])
def full(fileName):
    return render_template('video.html', data=fileName)


@app.route("/edited/<fileName>", methods=["GET"])
def edited(fileName):
    return render_template('edited_video.html', data=fileName)


@app.route("/uploads/<fileName>", methods=["GET"])
def show_video(fileName):
    path = UPLOAD_FOLDER + fileName
    return send_file(path, mimetype='multipart/form')


@app.route("/edit/<fileName>", methods=["GET"])
def show_edit_video(fileName):
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'edit_folder/')
    path = UPLOAD_FOLDER + fileName
    return send_file(path, mimetype='multipart/form')


app.register_blueprint(user_api, url_prefix='/api')
app.register_blueprint(full_api, url_prefix='/api')
app.register_blueprint(edit_api, url_prefix='/api')
app.register_blueprint(login_api)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port='5001',debug=True)


