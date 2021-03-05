import os
from pathlib import Path

import flask
import io
from tensorflow import keras

########### deep learning ##############
from c3d import *
from classifier import *
from utils.visualization_util import *
########################################
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



############## deep learning ##############
def run_demo(video_name):
    # read video
    new_video_path ='./input/'+video_name+'.mp4'
    video_clips, num_frames = get_video_clips(new_video_path)
    print("비디오 클립 수 : ", len(video_clips))

    # build models
    feature_extractor = c3d_feature_extractor()
    classifier_model = build_classifier_model()
    print("Models initialized")

    # extract features
    rgb_features = []
    for i, clip in enumerate(video_clips):
        clip = np.array(clip)
        if len(clip) < params.frame_count:
            continue
        clip = preprocess_input(clip)
        rgb_feature = feature_extractor.predict(clip)[0]
        rgb_features.append(rgb_feature)
        print("Processed clip : ", i)

    rgb_features = np.array(rgb_features)

    # bag features
    rgb_feature_bag = interpolate(rgb_features, params.features_per_bag)

    # classify using the trained classifier model
    predictions = classifier_model.predict(rgb_feature_bag)
    predictions = np.array(predictions).squeeze()
    predictions = extrapolate(predictions, num_frames)
    print("predictions:",predictions)

    # anomaly score txt 파일 저장
    anomaly_save_path = os.path.join(cfg.output_folder, video_name + '.txt')
    f = open(anomaly_save_path, 'w')
    for i in range(len(predictions)):
    	data = str('{:.2f}\n'.format(predictions[i]) )
    	f.write(data)
    f.close()

    # anomaly score 0.9 이상인 부분에 대해 앞뒤 1분 주기로 잘라서 mp4 저장
    edited_save_path = os.path.join(cfg.output_folder, video_name + '.mp4')
    get_edited_video(new_video_path, predictions, edited_save_path)
    print('Executed Successfully - ' + video_name + '.mp4 saved')

    '''
    # anomaly score 그래프 포함한 gif 저장
    video_save_path = os.path.join(cfg.output_folder, video_name + '.gif')
    visualize_predictions(new_video_path, predictions, video_save_path)
    print('Executed Successfully - ' + video_name + '.gif saved')
    '''

###############################################################################




## localhost:5000/anomaly_score
@app.route('/anomaly_score')
def get_anomaly_score():

    new_video_name = 'Explosion008_x264'
    new_video_path = './input/'+new_video_name+'.mp4'
    new_video_file = Path(new_video_path)

    # 지정한 파일명에 대한 비디오가 있을 때에만 딥러닝 영상분석 시작
    if new_video_file.is_file():
        run_demo(new_video_name)
        f = open('output/'+new_video_name+'.txt', 'r') # anomaly score txt 파일
        return "</br>".join(f.readlines())

    else:
        return "</br>".join("없습니다.")


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port='5001',debug=True, threaded=True)
