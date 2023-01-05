import cv2
import os
import numpy as np
from tqdm import tqdm
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
        if np.any(image[:, i, 1] != 255):
            start = i
            break
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
    num_frames = len(os.listdir(frame_path))
    fps = num_frames/duration
    
    # use ffmpeg to convert images to video
    os.system('ffmpeg -r {} -i {} -vcodec libx264 -crf 25  -pix_fmt yuv420p {}'.format(fps, frame_path+"/%d.png", video_path))
    print("Done with converting the image to video!")
