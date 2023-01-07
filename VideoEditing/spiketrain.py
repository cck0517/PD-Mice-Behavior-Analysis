import scipy.io as sio
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib_scalebar.scalebar import ScaleBar # pip install matplotlib-scalebar 
import cv2
from moviepy.editor import *
def spiketrain(spiketrain_path, recording_path, spiketrain_video, stacked_video, length_fraction=1/20, fps=1, show_axis=False, producing_video=False):
    """
    :param spiketrain_path: path to the spiketrain.mat file
    :param video_path: path to the recording video file (.mp4)
    :param spiketrain_video: path to store the spiketrain video
    :param stacked_video: path to store the stacked video
    :param length_fraction: the fraction of the length of the video that the scale bar should be, default is 1/20, if the scale bar is too long, it will cover the video
    :param fps: the fps of the generated video, default is 5, if the fps is too high, the animation will be too fast
    :param show_axis: whether to show the axis
    :param producing_video: whether to produce the video, if false, only show the animation in the python console
    :return: None
    """
    spiketrain = sio.loadmat(spiketrain_path)
    spike = spiketrain['spiketrain'] # spike is a 1D array
    # get the width and height of the video
    cap = cv2.VideoCapture(recording_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # in pixels
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # in pixels
    fig = plt.figure(1, figsize=(15 , 3)) 
    ax = fig.add_subplot()

    # get video length
    FPS = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Frame count: ", frame_count)
    duration = frame_count/FPS
    print("Video length: {} sec".format(duration))
    print(len(spike)/(duration*fps))
    animation_fps = int(len(spike)/(duration*fps))
    print("Animation fps: ", animation_fps)

    # Create scale bar
    scalebar = ScaleBar(dx=2, length_fraction=length_fraction, width_fraction=0.01, location='lower right', scale_formatter = lambda value, unit: f"{100} {'ms'}", color='black', box_color='white', box_alpha=1, frameon=False)         
    ax.add_artist(scalebar) 

    #rolling window size
    repeat_length = animation_fps*(100/1000)/length_fraction
    print("Repeat length: ", repeat_length)
    ax.set_xlim([0,repeat_length])
    ax.set_ylim([0, 5])
    line, = ax.plot([],[], c='black', lw=0.1)

    # hide the axis
    if not show_axis:
        ax.axis('off')
    def init():
        for f in range(0, animation_fps):
                if spike[f]>0:
                    ax.plot([f,f],[1,4], c='black')
                if f>repeat_length:
                    ax.set_xlim(f-repeat_length, f)
                else:
                    ax.set_xlim(0,repeat_length)
        return line,
    def animate(i):
        if i > 0:
            for f in range((i)*animation_fps, (i+1)*animation_fps):
                if spike[f]>0:
                    ax.plot([f,f],[1,4], c='black')
                if f>repeat_length:
                    ax.set_xlim(f-repeat_length, f)
                else:
                    ax.set_xlim(0,repeat_length)
        return line,

    anim = FuncAnimation(fig, animate, init_func=init, frames= round(duration*fps), interval=1, blit=False) # interval: delay between frames in milliseconds
    # save the animation as mp4 video file
    if producing_video:
        print('Start to produce spiketrain video ...')
        anim.save(spiketrain_video, fps=fps, extra_args=['-vcodec', 'libx264'])
        print('Done with producing and saving spiketrain video!')
        print('Start to stack recording video and spiketrain video ...')
        # stack the video and spiketrain video
        spiketrain = VideoFileClip(spiketrain_video)
        cap = cv2.VideoCapture(spiketrain_video)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # in pixels
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # in pixels
        print("Video width: ", width)
        print("Video height: ", height)
        recording = VideoFileClip(recording_path)
        recording = recording.on_color(size=(1280, 1324), color=(255, 255, 255), pos=(100, 300))
        spiketrain = spiketrain.on_color(size = (1550, 500), color=(255, 255, 255), pos=(50, 200)) # pos is the position of the video in width and height
        final = [[recording], [spiketrain]]
        final = clips_array(final)
        final = final.on_color(size=(1600, 2000), color=(255, 255, 255), pos=(0, 0))  
        final.write_videofile(stacked_video, fps=30)
    else:
        plt.show()

spiketrain_path = 'spiketrain.mat'
recording_path = 'recording.mp4'
spiketrain_video = 'spiketrain.mp4'
stacked_video = 'stacked.mp4'

# spiketrain(spiketrain_path, recording_path, spiketrain_video, stacked_video, length_fraction=1/20, fps=5, show_axis=True, producing_video=False)