import os

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
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads/')

@login_manager.user_loader
def load_user(user_id):
    return USERS[user_id]


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



############## deep learning ##############
def run_demo():
    video_name = os.path.basename(cfg.sample_video_path).split('.')[0]

    # read video
    video_clips, num_frames = get_video_clips(cfg.sample_video_path)

    print("Number of clips in the video : ", len(video_clips))

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
    
    
    #for i in range(len(predictions)):
    	#print(predictions[i])

    save_path = os.path.join(cfg.output_folder, video_name + '.txt')
    
    f = open(save_path, 'w')
    for i in range(len(predictions)):
    	data = str(predictions[i]) + '\n'
    	f.write(data)
    f.close()
    
    
    # visualize predictions
    visualize_predictions(cfg.sample_video_path, predictions, save_path)
    print('Executed Successfully - ' + video_name + '.gif saved')
###############################################################################    
    
    

## localhost:5000/anomaly_score
@app.route('/anomaly_score')
def get_anomaly_score():

    ### deeplearning ### 
    run_demo()
    #####################
    
    fileName = 'Normal_Videos_006_x264'
    f = open('output/'+fileName+'.txt', 'r')
    
    return "</br>".join(f.readlines())

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0',port='5001',debug=True, threaded=True)



