import spiketrain as spt
import imageToVideo as itv
from moviepy.editor import *
import streamlit as st
import os
import time

st.set_page_config(page_title='stack video', page_icon="📊",
                   layout='wide', initial_sidebar_state='auto')
st.header('Synchronize recording with EEG, EMG and Spiketrain data')
st.subheader('Load data and process')
image_path = st.text_input('Enter the image directory', os.getcwd())
try:
    st.markdown('You have selected **{}** as your image_path'.format(image_path))
except FileNotFoundError:
    st.error('No such directory')
recording_path = st.text_input('Enter the recording directory', os.getcwd())
try:
    st.markdown('You have selected **{}** as your recording directory'.format(recording_path))
except FileNotFoundError:
    st.error('No such directory')
frame_path = os.getcwd() + "/frames"
video_path = os.getcwd() + "/EEG_EMG_SpikeRate_Video.mp4"
if st.button("Start converting image to video"):
    try:
        itv.imageToVideo(image_path, frame_path, recording_path, video_path)
        my_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        st.markdown('The video is stored in **{}**'.format(video_path))
    except FileNotFoundError:
        st.error('Path might be wrong')
if st.button("Show video"):
    try:
        video_file = open(video_path, 'rb') 
        video_bytes = video_file.read()
        st.video(video_bytes)
    except FileNotFoundError:
        st.markdown('Video path: **{}**'.format(video_path))
        st.error('No such video')
    # spt.spiketrain(spiketrain_path, recording_path, spiketrain_video, stacked_video, length_fraction=1/20, fps=5, show_axis=False, producing_video=True)

    # # stack the two videos
    # left_clip = VideoFileClip(spiketrain_video)
    # right_clip = VideoFileClip(video_path)
    # final_clip = concatenate_videoclips([left_clip, right_clip])
    # final_clip.write_videofile(stacked_video, fps=30)






