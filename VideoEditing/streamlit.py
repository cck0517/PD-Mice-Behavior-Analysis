import spiketrain as spt
import imageToVideo as itv
from moviepy.editor import * 
import streamlit as st
import os
import time
import cv2
st.set_page_config(page_title='stack video', page_icon="📊",
                     layout='wide', initial_sidebar_state='auto')
st.header('Synchronize recording with EEG, EMG and Spiketrain data')

recording_path = st.text_input('Enter the path to the video recording', os.getcwd())
if not os.path.isfile(recording_path):
    st.error('No such file')
image_path = st.text_input('Enter the path to the image', os.getcwd())
if not os.path.isfile(image_path):
    st.error('No such file')
frame_path = os.getcwd() + "/frames"
video_path = os.getcwd() + "/EEG_EMG_SpikeRate_Video.mp4"
spiketrain_path = st.text_input('Enter the path to the spiketrain matfile', os.getcwd())
if not os.path.isfile(spiketrain_path):
    st.error('No such file')

    
spiketrain_video = os.getcwd() + "/spiketrain.mp4"
stacked_video = os.getcwd() + "/stacked.mp4" # video with spiketrain and recording

st.markdown('### Spiketrain animation settings')
st.markdown('#### length_fraction')
st.markdown('The length fraction determines the length of the scale bar relative to the length of the animation rolling window.')
length_fraction = st.slider('length fraction', min_value=0.0, max_value=1.0, value=0.05, step=0.1)
st.markdown('#### frame rate')
st.markdown('The frame rate determines the how fast the animation will be played.')
fps = st.slider('frame rate', min_value=0, max_value=60, value=5, step=1)
final_video = os.getcwd() + "/final_video.mp4"
st.text_input('Video generated will be stored in the following path', final_video)

if st.button('Generate video'):
    if os.path.exists(video_path):
        os.remove(video_path)
    itv.imageToVideo(image_path, frame_path, recording_path, video_path)
    spt.spiketrain(spiketrain_path, recording_path, spiketrain_video, stacked_video, length_fraction=length_fraction, fps=fps, show_axis=False, producing_video=True)
    right = VideoFileClip(video_path)
    right = right.resize((1600, 2000))
    right = right.on_color(size=(1600, 2000), color=(255, 255, 255), pos=(0, 100))
    left = VideoFileClip(stacked_video)
    final_clip = clips_array([[left, right]])
    final_clip.write_videofile("final.mp4", fps=30)
    os.remove(video_path)
    os.remove(stacked_video)
    os.remove(spiketrain_video)
    st.success('Video generated')

