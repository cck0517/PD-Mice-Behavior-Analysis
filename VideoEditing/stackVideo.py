from moviepy.editor import *
import os
current_path = os.getcwd()
recording = VideoFileClip(current_path + "/VideoEditing/recording.mp4")
# show the width and height of the video
print(recording.w, recording.h)
EEG = VideoFileClip(current_path + "/VideoEditing/EEG.mp4")
# chang the speed of the video
EEG = EEG.fx(vfx.speedx, 0.3152)
# change the size of the video
EEG = EEG.resize((1280, 400))
print(EEG.w, EEG.h)
spiketrain = VideoFileClip(current_path + "/VideoEditing/spiketrain.mp4")
spiketrain.resize((1280, 400))
print(spiketrain.w, spiketrain.h)
EMG_FireRate = VideoFileClip(current_path + "/VideoEditing/EMG_FireRate.mp4")
# match the duration of EMG_FireRate to EEG
EMG_FireRate = EMG_FireRate.subclip(0, 184) 
EMG_FireRate = EMG_FireRate.resize((1280, 1000))
print(EMG_FireRate.w, EMG_FireRate.h)
clips = [[recording, spiketrain],[EEG, EMG_FireRate]]
final = clips_array(clips)
# change the background color
final = final.on_color(size=(1280, 2000), color=(255, 255, 255), pos=(0, 0))
final.write_videofile(current_path + "/VideoEditing/final_video.mp4", fps=60)
