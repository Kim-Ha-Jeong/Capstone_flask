import os

from c3d import *
from classifier import *
from utils.visualization_util import *

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

    anomaly_save_path = os.path.join(cfg.output_folder, video_name + '.txt')

    f = open(anomaly_save_path, 'w')
    for i in range(len(predictions)):
    	data = str(predictions[i]) + '\n'
    	f.write(data)
    f.close()

    # anomaly score 그래프 포함한 gif 저장
    video_save_path = os.path.join(cfg.output_folder, video_name + '.gif')
    visualize_predictions(cfg.sample_video_path, predictions, video_save_path)
    print('Executed Successfully - ' + video_name + '.gif saved')


    # anomaly score 0.9 이상인 부분에 대해 앞뒤 1분 주기로 잘라서 mp4 저장
    edited_save_path = os.path.join(cfg.output_folder, video_name + '.mp4')
    get_edited_video(cfg.sample_video_path, predictions, edited_save_path)
    print('Executed Successfully - ' + video_name + '.mp4 saved')


if __name__ == '__main__':
    run_demo()
