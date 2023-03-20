import spiketrain as spt
import imageToVideo as itv
from moviepy.editor import * 
import os
import time
import cv2

#################### Path and amination settings ####################
image_path = "Feeding.png" # path to the image
recording_path = "recording.mp4" # path to the video recording
spiketrain_path = "spiketrain.mat" # path to the spiketrain matfile
final_video_path = "final_test.mp4" # path where the final video will be stored
# length_fraction determines the length of the scale bar relative 
# to the length of the animation rolling window.
# The larger the value, the longer the scale bar will be.
length_fraction = 0.001
# frame rate determines the how fast the animation will be played.
# The larger the value, the faster the animation will be played.
fps = 30
#####################################################################

spiketrain_video = "spiketrain.mp4"
stacked_video = "stacked_test.mp4"
frame_path = "frames"
video_path = "video.mp4"

# os.remove(video_path)
# os.remove(stacked_video)
# os.remove(spiketrain_video)
'''
itv.imageToVideo(image_path, frame_path, recording_path, video_path)
# spt.spiketrain(spiketrain_path, recording_path, spiketrain_video, stacked_video, length_fraction=length_fraction, fps=fps, show_axis=False, producing_video=True)
right = VideoFileClip(video_path)
cap = cv2.VideoCapture(video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
right = right.resize((round(width*3.5), round(height*3.5)))
right = right.on_color(size=(2000, 2800), color=(255, 255, 255))
left = VideoFileClip(stacked_video)
final_clip = clips_array([[left, right]])
'''
# slow down the video
path = "final_video_normal_speed.mp4"
final_clip = VideoFileClip(path) 
final_clip = final_clip.fx(vfx.speedx, 2/3)
final_clip.write_videofile(final_video_path, fps=30)
