from fulls import *
from users import *
from login import *

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


@app.route("/uploads/<fileName>", methods=["GET"])
def show_video(fileName):
    path = UPLOAD_FOLDER + fileName
    return send_file(path, mimetype='video')


app.register_blueprint(user_api, url_prefix='/api')
app.register_blueprint(full_api, url_prefix='/api')
app.register_blueprint(login_api)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001',debug=True)


