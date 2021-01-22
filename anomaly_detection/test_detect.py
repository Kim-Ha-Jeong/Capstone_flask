import os
from pathlib import Path

from anomaly_detection.c3d import *
from anomaly_detection.classifier import *
import anomaly_detection.configuration as cfg
from anomaly_detection.utils.visualization_util import *

def run_demo(video_name):
    # read video
    new_video_path =os.path.join(cfg.input_folder, video_name + '.mp4')
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


if __name__ == '__main__':
    new_video_name = 'Explosion008_x264'
    new_video_path = os.path.join(cfg.input_folder, new_video_name + '.mp4')
    new_video_file = Path(new_video_path)

    # 지정한 파일명에 대한 비디오가 있을 때에만 딥러닝 영상분석 시작
    if new_video_file.is_file():
        print("딥러닝 영상분석 실행")
        run_demo(new_video_name)

    else:
        print("딥러닝 영상분석 실행 X (파일 없음)")
