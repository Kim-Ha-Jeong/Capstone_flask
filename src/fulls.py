import os
from flask import request, redirect
from flask_login import login_required
from werkzeug.utils import secure_filename
import time
from src.login import *

from src.database import engine
from src.extensions import allowed_file

import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from . import video_analysis

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../input/')

full_api = Blueprint('full_api', __name__)


# 파일 업로드
@full_api.route('/full', methods=['POST'])
@login_required
def upload():
        f = request.files['full_video']  #파일 이름
        user = current_user  #로그인된 user

        user_id = user.get_id()
        result = engine.execute("select * from full where user_id=%s", user_id)
        i: int = 1
        for x in result:
            i = i+1  #user가 저장한 파일 수

        vname = "full0"+str(user_id)+"0"+str(i)
        fname = "full0"+str(user_id)+"0"+str(i)+".mp4" #저장할 파일이름 생성

        path = UPLOAD_FOLDER + fname  #저장할 경로 설정

        full_video = fname
        date = time.strftime("%Y-%m-%d %H:%M:%S")  #업로드한 날짜
        storage_path = '/input/'+ fname

        if allowed_file(f.filename):  #동영상 파일
            f.save(path)   # 파일 저장
            size = os.stat(path).st_size  # 파일 크기
            engine.execute("insert into full (full_video,date,size,storage_path, user_id) "
                           "values (%s, %s, %s, %s, %s)", full_video, date, size, storage_path, user_id)

            get_anomaly_score(vname) # 딥러닝 영상분석 결과 저장

            return full_video
        else:
            return "error"


# 저장된 목록 모두 불러옴
@full_api.route('/full', methods=['GET'])
@login_required
def full_list():
    user_id = current_user
    result = engine.execute("select * from full where user_id=%s",user_id.get_id())
    return render_template('full.html', datas=result, mimetype='application/json')


@full_api.route('/full/<id>', methods=['GET'])
def show(id):
    result = engine.execute("select * from full where id=%s",id)

    return render_template('full_update.html', datas=result)


# 동영상 정보 업데이트
@full_api.route('/full/<id>', methods=['POST'])
def update(id):
    parser = reqparse.RequestParser()
    parser.add_argument('full_video', type=str)
    parser.add_argument('date', type=str)
    parser.add_argument('size', type=str)
    parser.add_argument('storage_path', type=str)
    parser.add_argument('user_id', type=str)
    args = parser.parse_args()

    full_video = args['full_video']
    date = args['date']
    size = args['size']
    storage_path = args['storage_path']
    user_id = args['user_id']

    engine.execute("update full set date=%s,size=%s,user_id=%s where id=%s", date, size, user_id, id)
    return redirect("/api/full")

# 동영상 삭제
@full_api.route('/full/delete/<id>', methods=['GET'])
def delete(id):
    engine.execute("delete from full where id=%s", id)
    return redirect("/api/full")
