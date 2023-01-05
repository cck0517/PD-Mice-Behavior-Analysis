import spiketrain as spt
import imageToVideo as itv
from moviepy.editor import *
import streamlit as st
import os
import time

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
    try:
        itv.imageToVideo(image_path, frame_path, recording_path, video_path)
        spt.spiketrain(spiketrain_path, recording_path, spiketrain_video, length_fraction=length_fraction, fps=fps, show_axis=False, producing_video=False)
        left_clip = VideoFileClip(spiketrain_video)
        right_clip = VideoFileClip(video_path)
        final_clip = concatenate_videoclips([left_clip, right_clip])
        final_clip.write_videofile(final_video, fps=30)
    except:
        st.error('Something went wrong')
