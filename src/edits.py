import os
from flask import request,redirect
from flask_login import login_required
from werkzeug.utils import secure_filename
import time

from src.extensions import allowed_file
from src.login import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '../output/')

edit_api = Blueprint('edit_api', __name__)


# 편집된 동영상 목록
@edit_api.route('/edited', methods=['GET'])
@login_required
def edited_list():
    user = current_user
    result = engine.execute("select * from edited where user_id=%s",user.get_id())

    return render_template('edited.html', datas=result)


@edit_api.route('/edited/<id>', methods=['GET'])
def show(id):
    result = engine.execute("select * from edited where id=%s",id)

    return render_template('edited_update.html', datas=result)


@edit_api.route('/edited/delete/<id>', methods=['GET'])
def delete(id):
    engine.execute("delete from edited where id=%s", id)
    return redirect("/api/edited")


@edit_api.route('/edited/count', methods=['GET'])
@login_required
def total_num():
    user = current_user
    user_id = user.get_id()
    num = engine.execute("select count(*) from full where user_id=%s", user_id)
    user_video = int(num.first()[0])
    arr = str(user_video)

    for i in range(user_video):
        arr = arr + str(engine.execute("select count(*) from edited where user_id=%s and full_id=%s", user_id, i+1).first()[0])
    return arr


# 편집된 동영상 정보 저장
def save():
    file_list = os.listdir(UPLOAD_FOLDER)
    i = 0
    for x in file_list:
        if ".mp4" in x:
            f = UPLOAD_FOLDER + x
            fname = f.split("/")
            list = x.split("0")

            flag = 0

            saved = engine.execute("select * from edited")
            for y in saved:
                if y.edited_video == fname[-1]:
                    print(fname[-1]+" "+y.edited_video)
                    flag  = 1
                    break

            if flag == 1:
                continue

            edited_video = fname[-1]
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            size = os.stat(f).st_size
            path = '/output/' + fname[-1]

            part_id = ''.join(list[3])
            part = part_id.replace('.mp4', '')

            engine.execute("insert into edited (edited_video, date, size, path, part, user_id, full_id) "
                               "values (%s, %s, %s, %s, %s, %s, %s)", edited_video, date, size, path, part, list[1],
                               list[2])
            i = i + 1

    return str(i)+" rows add"


@edit_api.route('/edited/save', methods=['GET'])
def syn():
    file_list = os.listdir(UPLOAD_FOLDER)
    i = 0
    for x in file_list:
        if ".mp4" in x:
            f = UPLOAD_FOLDER + x
            fname = f.split("/")
            list = x.split("0")

            flag = 0

            saved = engine.execute("select * from edited")
            for y in saved:
                if y.edited_video == fname[-1]:
                    print(fname[-1]+" "+y.edited_video)
                    flag  = 1
                    break

            if flag == 1:
                continue

            edited_video = fname[-1]
            date = time.strftime("%Y-%m-%d %H:%M:%S")
            size = os.stat(f).st_size
            path = '/output/' + fname[-1]

            part_id = ''.join(list[3])
            part = part_id.replace('.mp4', '')

            engine.execute("insert into edited (edited_video, date, size, path, part, user_id, full_id) "
                               "values (%s, %s, %s, %s, %s, %s, %s)", edited_video, date, size, path, part, list[1],
                               list[2])
            i = i + 1

    return str(i)+" rows add"