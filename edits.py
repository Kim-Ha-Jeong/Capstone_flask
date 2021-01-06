import os
from flask import request, jsonify, send_file, Blueprint, render_template, redirect
from flask_restful import reqparse
from werkzeug.utils import secure_filename
import time

from database import engine
from extensions import allowed_file

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'edit_folder/')

edit_api = Blueprint('edit_api', __name__)


@edit_api.route('/edited', methods=['POST'])
def upload():
        f = request.files['edited_video']

        fname = secure_filename(f.filename)

        e_path = UPLOAD_FOLDER + fname

        parser = reqparse.RequestParser()
        parser.add_argument('anomaly_score', type=str)
        args = parser.parse_args()

        edited_video = fname
        date = time.strftime("%Y-%m-%d %H:%M:%S")
        path = '/edit_folder/'+fname
        anomaly_score = args['anomaly_score']

        if allowed_file(f.filename):
            f.save(e_path)
            size = os.stat(e_path).st_size
            engine.execute("insert into edited (edited_video, anomaly_score, date, size,path, user_id, full_id) "
                           "values (%s, %s, %s, %s, %s, %s, %s)", edited_video, anomaly_score, date, size, path, 1,1)

            return "ok"
        else:
            return "error"


@edit_api.route('/edited', methods=['GET'])
def full_list():
    result = engine.execute("select * from edited")

    return render_template('edited.html', datas=result)


@edit_api.route('/edited/<id>', methods=['GET'])
def show(id):
    result = engine.execute("select * from edited where id=%s",id)

    return render_template('edited_update.html', datas=result)


@edit_api.route('/edited/<id>', methods=['POST'])
def update(id):
    parser = reqparse.RequestParser()
    parser.add_argument('anomaly_score', type=str)
    args = parser.parse_args()

    anomaly_score = args['anomaly_score']

    engine.execute("update edited set anomaly_score=%s where id=%s", anomaly_score, id)
    return redirect("/api/edited")


@edit_api.route('/edited/delete/<id>', methods=['GET'])
def delete(id):
    engine.execute("delete from edited where id=%s", id)
    return redirect("/api/edited")

