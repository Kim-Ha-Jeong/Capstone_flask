# anomaly score txt file save
import os

from h5py.h5t import cfg

anomaly_save_path = os.path.join(cfg.output_folder, video_name + '.txt')
f = open(anomaly_save_path, 'w')
for i in range(len(predictions)):
    data = str('{:.2f}\n'.format(predictions[i]))
    f.write(data)
f.close()

# extract video
edited_save_path = os.path.join(cfg.output_folder, 'edited' + video_name[4:9] + video_num + '.mp4')
get_edited_video(new_video_path, predictions, edited_save_path)
print('Executed Successfully - ' + video_name + '.mp4 saved')

'''
# anomaly score graph gif save
video_save_path = os.path.join(cfg.output_folder, video_name + '.gif')
visualize_predictions(new_video_path, predictions, video_save_path)
print('Executed Successfully - ' + video_name + '.gif saved')
'''

