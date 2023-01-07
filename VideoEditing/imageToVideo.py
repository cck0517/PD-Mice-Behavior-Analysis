import cv2
import os
import numpy as np
from tqdm import tqdm
from moviepy.editor import *
def imageToVideo(image_path, frame_path, recording_path, video_path):
    """
    :param image_path: path to the image
    :param frame_path: path to the folder where the sliced images will be saved
    :param recording_path: path to the recording video
    :param video_path: path to store video
    :param fps: frames per second of the generated video
    """
    # Make frame path if it does not exist
    if not os.path.exists(frame_path):
        os.makedirs(frame_path)
    # Read image
    image = cv2.imread(image_path)
    # Image shape 
    height = image.shape[0]
    width = image.shape[1]
    start, end = 0, width
    # Find the minimum and maximum width of the colored region
    for i in range(width):
        # convert a list to set
        if np.all(image[:, i, 1] != 255):
            start = i
            break
    start = 50
    for i in range(width//2, width):
        if np.all(image[:, i, 1] == 255):
            end = i
            break
    # Make an empty image
    empty = np.zeros((height, width, 3), dtype=np.uint8)
    # fill in the values of empty with 255
    empty.fill(255)
    for i in tqdm(range(start, end)):
        empty[:height, :i, 0] = image[:height, :i, 0]
        empty[:height, :i, 1] = image[:height, :i, 1]
        empty[:height, :i, 2] = image[:height, :i, 2]
        # save the image
        cv2.imwrite(frame_path + "/" + str(i-start) + ".png", empty)
    print('Done with slicing the image')


    cap = cv2.VideoCapture(recording_path)
    FPS = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/FPS
    print("Duration of the video: ", duration)
    num_frames = len(os.listdir(frame_path))
    fps = num_frames/duration
    print("FPS of the video: ", fps)

    # use ffmpeg to convert images to video
    os.system('ffmpeg -r {} -i {} -vcodec libx264 -crf 25  -pix_fmt yuv420p {}'.format(fps, frame_path+"/%d.png", video_path))
    print("Done with converting the image to video!")
    # delete the frames in the frame_path
    for file in os.listdir(frame_path):
        os.remove(os.path.join(frame_path, file))

# image_path = "Feeding.png"
# frame_path = "frames"
# recording_path = "recording.mp4"
# video_path = "video.mp4"
# # imageToVideo(image_path, frame_path, recording_path, video_path)
# stacked_video = "stacked.mp4"
# cap = cv2.VideoCapture(video_path)
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # in pixels
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # in pixels
# print("Video width: ", width)
# print("Video height: ", height)
# right = VideoFileClip(video_path)
# right = right.resize((1600, 2000))
# right = right.on_color(size=(1600, 2000), color=(255, 255, 255), pos=(0, 100))
# left = VideoFileClip(stacked_video)
# final_clip = clips_array([[left, right]])
# final_clip.write_videofile("final.mp4", fps=30)
