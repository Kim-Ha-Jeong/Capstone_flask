import os
from flask import request, jsonify, send_file, Blueprint
from flask_restful import reqparse
from werkzeug.utils import secure_filename

from database import engine
from extensions import allowed_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads/')

full_api = Blueprint('full_api', __name__)


@full_api.route('/full', methods=['POST'])
def upload():
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


@full_api.route('/full', methods=['GET'])
def full_list():
    result = engine.execute("select * from full")

    return jsonify([dict(row) for row in result])


@full_api.route("/full/<fileName>", methods=["GET"])
def full(fileName):
    return send_file(UPLOAD_FOLDER+fileName, mimetype='video')

