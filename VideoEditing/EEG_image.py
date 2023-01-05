import cv2
import os
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
current_path = os.getcwd()
# Read image
image = cv2.imread(current_path + "/VideoEditing/EEGpsd.png")

# image to values 
print(image.shape) # (1486, 3840, 3)

empty = np.zeros((400, 3840, 3), dtype=np.uint8)
# fill in the values of empty with 255
empty.fill(255)
for i in range(190, 3650):
    empty[:400, :i, 0] = image[:400, :i, 0]
    empty[:400, :i, 1] = image[:400, :i, 1]
    empty[:400, :i, 2] = image[:400, :i, 2]
    # save the image
    cv2.imwrite(current_path + "/VideoEditing/EEG_new/" + str(i-190) + ".png", empty)   
print("Done")

for i in range(3600, 3700):
    if image[200, i, 1] == 255:
        print(i)
        break
# colored region 190:3649

# use ffmpeg to convert images to video
os.system('ffmpeg -r 18.8 -i VideoEditing/EEG_new/%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p VideoEditing/EEG_2.mp4')
print("Done")