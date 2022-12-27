import os
from tqdm import tqdm
import pandas as pd

# Use ffmpeg command to convert video to frames
#os.system('ffmpeg -i /BSOID_2.34/2022-12-17 22-34-43.mp4 -r 60 -f image2 frames/image-%03d.png')

# Read in the data
df = pd.read_csv('BSOID_2.34/Dec-24-2022_2022-12-17 22-34-43bout_lengths_60Hz2022-12-17 22-34-43DLC_resnet50_CylinderBottomViewDec18shuffle1_1030000.csv')

if not os.path.exists('video snippets'):
    os.makedirs('video snippets')

last = 0
for i in tqdm(range(1, len(df))):
    # Read the first line in the csv file
    line = df.iloc[0]
    # Get B-SOiD labels for the first line
    labels = line[1]
    if not os.path.exists('video snippets/' + str(labels)):
        os.makedirs('video snippets/' + str(labels))
    # Get the video length 
    video_start = last + line[2]
    video_end = video_start + line[3]
    # Use ffmpeg command to extract the video snippet and save it to the corresponding folder 
    os.system(('ffmpeg -ss {} -i BSOID_2.34/test.mp4 -to {} -c copy -copyts BSOID_2.34/video_snippets/{}/video-{}.mp4').format(video_start, video_end, labels, video_start))
    last = video_end

