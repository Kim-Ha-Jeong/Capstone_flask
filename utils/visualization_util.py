import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from utils.video_util import *

import cv2
import numpy as np
import os
from os.path import isfile, join


def visualize_clip(clip, convert_bgr=False, save_gif=False, file_path=None):
    num_frames = len(clip)
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    def update(i):
        if convert_bgr:
            frame = cv2.cvtColor(clip[i], cv2.COLOR_BGR2RGB)
        else:
            frame = clip[i]
        plt.imshow(frame)
        return plt

    # FuncAnimation will call the 'update' function for each frame; here
    # animating over 10 frames, with an interval of 20ms between frames.
    anim = FuncAnimation(fig, update, frames=np.arange(0, num_frames), interval=1)
    if save_gif:
        anim.save(file_path, dpi=80, writer='imagemagick')
    else:
        # plt.show() will just loop the animation forever.
        plt.show()


def visualize_predictions(video_path, predictions, save_path):
    frames = get_video_frames(video_path)
    assert len(frames) == len(predictions)

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.set_tight_layout(True)

    fig_frame = plt.subplot(2, 1, 1)
    fig_prediction = plt.subplot(2, 1, 2)
    fig_prediction.set_xlim(0, len(frames))
    fig_prediction.set_ylim(0, 1.15)

    def update(i):
        frame = frames[i]
        x = range(0, i)
        y = predictions[0:i]
        fig_prediction.plot(x, y, '-')
        fig_frame.imshow(frame)
        return plt

    # FuncAnimation will call the 'update' function for each frame; here
    # animating over 10 frames, with an interval of 20ms between frames.

    anim = FuncAnimation(fig, update, frames=np.arange(0, len(frames), 10), interval=1, repeat=False)

    if save_path:
        plt.show()
        anim.save(save_path, writer='imagemagick', fps=30)
    else:
        plt.show()

    return



def get_edited_video(video_path, predictions, save_path):
    # anomaly score 가 0.9 이상인 부분에 대해 앞뒤 1분간격으로 저장하는 코드 작성해야함
    frames = get_video_frames(video_path)
    assert len(frames) == len(predictions)

    outpath = save_path
    fps = 30
    size =  (frames[0].shape[1],frames[0].shape[0])
    print(size)

    # 0.9 이상인 부분에 대해 앞뒤 1분주기로 자르는 알고리즘
    # 1분 = 60*30 프레임

    first_frame = 0
    last_frame = len(frames)-1
    anomaly_first = -1
    anomaly_last = -1

    for i in range(len(frames)):
        if predictions[i]>=0.9:
            if(anomaly_first== -1):
                anomaly_first = i
            anomaly_last = i

    edit_first = anomaly_first - 1800
    edit_last = anomaly_last + 1800

    if(edit_first<first_frame):
        edit_first = first_frame
    if(edit_last>last_frame):
        edit_last = last_frame

    edit_frames = frames[edit_first:edit_last]

    # 모두 정상적인 경우 저장하지 않음
    if(anomaly_first==-1 & anomaly_last==-1):
        print("정상 비디오")
        return

    # 동영상 저장
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter(save_path,fourcc, fps, size)
    for i in range(len(edit_frames)):
       frames[i] = cv2.cvtColor(edit_frames[i], cv2.COLOR_BGR2RGB)
       out.write(edit_frames[i])
    out.release()


    return
