from flask_restful import reqparse, Api
from flask import Flask, jsonify, request, send_file
from werkzeug.utils import secure_filename

from database import *
import os
from extensions import *

app = Flask(__name__)
api = Api(app)


@app.route('/user', methods=['POST'])
def sign_up():
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str)
    parser.add_argument('password', type=str)
    args = parser.parse_args()

    email = args['email']
    password = args['password']

    engine.execute("insert into user (email,password) values (%s, %s)", email, password)

    return {'email': email, 'password': password}


@app.route('/user', methods=['GET'])
def user_list():
    result = engine.execute("select * from user")

    return jsonify([dict(row) for row in result]);


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads/')


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        f = request.files['full_video']
        fname = secure_filename(f.filename)

        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str)
        parser.add_argument('size', type=str)
        parser.add_argument('storage_path', type=str)
        parser.add_argument('user_id', type=int)
        args = parser.parse_args()

        full_video = fname
        date = args['date']
        size = args['size']
        storage_path = args['storage_path']
        user_id = args['user_id']

        path = UPLOAD_FOLDER + fname

        if allowed_file(f.filename):
            engine.execute("insert into full (full_video,date,size,storage_path,user_id) "
                           "values (%s, %s, %s, %s, %s)", full_video, date, size, storage_path, user_id)
            f.save(path)
            return "ok"
        else:
            return "error"


@app.route("/upload", methods=["GET"])
def full_list():
    result = engine.execute("select * from full")

    return jsonify([dict(row) for row in result]);


@app.route("/image/<fileName>", methods=["GET", "POST"])
def full(fileName):
    return send_file(UPLOAD_FOLDER+fileName, mimetype='video')


if __name__ == '__main__':
    app.run(debug=True)
