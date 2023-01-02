from moviepy.editor import *
import os
current_path = os.getcwd()
spiketrain = VideoFileClip(current_path + "/VideoEditing/spiketrain.mp4")
spiketrain = spiketrain.resize((1520, 500))
recording = VideoFileClip(current_path + "/VideoEditing/recording.mp4")
recording = recording.margin(50, 50, 150, 150, color=(255, 255, 255)) # 0 is top, 1 is right, 2 is bottom, 3 is left
# change the color of the margin
recording = recording.on_color(size=(1280, 1000), color=(255, 255, 255), pos=(0, 0))
EMG_FireRate = VideoFileClip(current_path + "/VideoEditing/EMG_FireRate.mp4")
EMG_FireRate = EMG_FireRate.resize((1400, 1000))
EEG = VideoFileClip(current_path + "/VideoEditing/EEG.mp4")
EEG = EEG.resize((1400, 1000))
clips = [[recording, EEG],[spiketrain, EMG_FireRate]]
final = clips_array(clips)
# change the background color
final = final.on_color(size=(1580*2, 2200), color=(255, 255, 255), pos=(0, 0))
final.write_videofile(current_path + "/VideoEditing/final_video.mp4", fps=60)
