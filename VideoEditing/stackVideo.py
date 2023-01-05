import spiketrain as spt
import imageToVideo as itv
from moviepy.editor import *
import streamlit as st
import os
import time

st.set_page_config(page_title='stack video', page_icon="📊",
                   layout='wide', initial_sidebar_state='auto')
st.header('Synchronize recording with EEG, EMG and Spiketrain data')

recording_path = st.text_input('Enter the path to the recording video of the mouse', os.getcwd())
if not os.path.isfile(recording_path):
    st.error('No such directory')

if st.sidebar.checkbox("Covert Image to Video", False):
    st.header('Convert Image to Video')
    image_path = st.text_input('Enter the path to the image', os.getcwd())
    if not os.path.isfile(image_path):
        st.error('No such directory')
    frame_path = os.getcwd() + "/frames"
    video_path = os.getcwd() + "/EEG_EMG_SpikeRate_Video.mp4"
    video_path = st.text_input('Video generated will be stored in the following path', video_path)
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

if st.sidebar.checkbox("Stack Spiketrain with recording", False):
    st.header('Stack Spiketrain with recording')
    spiketrain_path = st.text_input('Enter the path to the spiketrain matfile', os.getcwd())
    if not os.path.isfile(spiketrain_path):
        st.error('No such directory')
    if st.button("Process spiketrain"):
        st.markdown('length_fraction dertermines the length of scale bar in the video. If the scale bar is too long, it will cover the video')
        length_fraction = st.slider('length_fraction', min_value=0.0, max_value=1.0, value=1/20, step=0.01)
        st.markdown('fps determines how fast the animation will be. The higher the fps, the faster the animation')
        fps = st.slider('frame rate', min_value=0, max_value=60, value=5, step=1)
        if st.checkbox('Show spiketrain rolling window only'):
            spiketrain_video = os.getcwd() + "/spiketrain.mp4"
            if st.checkbox('Show axis'):
                show_axis = True
            else:
                show_axis = False
            spt.spiketrain(spiketrain_path, recording_path, spiketrain_video, length_fraction=length_fraction, fps=fps, show_axis=show_axis,producing_video=False)
        
        if st.checkbox('Producing stacked video'):
            spiketrain_video = os.getcwd() + "/spiketrain.mp4"
            st.text_input('Video generated will be stored in the following path', spiketrain_video)
            producing_video = True
            stacked_video = os.getcwd() + "/stacked_video.mp4"
            st.text_input('Video generated will be stored in the following path', stacked_video)
            spt.spiketrain(spiketrain_path, recording_path, spiketrain_video, stacked_video, length_fraction=length_fraction, fps=fps, show_axis=False, producing_video=True)

        if st.button("Show spiketrain video"):
            try:
                spiketrain_video = os.getcwd() + "/spiketrain.mp4"
                video_file = open(spiketrain_video, 'rb') 
                video_bytes = video_file.read()
                st.video(video_bytes)
            except FileNotFoundError:
                st.markdown('Video path: **{}**'.format(spiketrain_video))
                st.error('No such video')

if st.sidebar.checkbox("Stack Video", False):
    final_video = os.getcwd() + "/final_video.mp4"
    st.text_input('Video generated will be stored in the following path', final_video)
    if st.button("Stack"):
        try:
            left_clip = VideoFileClip(spiketrain_video)
            right_clip = VideoFileClip(video_path)
            final_clip = concatenate_videoclips([left_clip, right_clip])
            final_clip.write_videofile(final_video, fps=30)
        except FileNotFoundError:
            st.error('File path might be wrong')






