# deep learning
from anomaly_detection.test_detect import *
import anomaly_detection.configuration as cfg

def get_anomaly_score(fileName):
    new_video_name = fileName
    new_video_path = os.path.join(cfg.input_folder, new_video_name+'.mp4')
    new_video_file = Path(new_video_path)

    # 지정한 파일명에 대한 비디오가 있을 때에만 딥러닝 영상분석 시작
    if new_video_file.is_file():
        run_demo(new_video_name)
        return 'ok'

    else:
        return 'error'
