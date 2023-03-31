import pandas as pd
import select_roi as sr
import numpy as np
import matplotlib.pyplot as plt
import hdbscan
from sklearn.mixture import GaussianMixture

# load the dataframe
Dataframe = pd.read_csv("test_group2/test.csv")
# replace '--' with 10
Dataframe = Dataframe.replace("--", 10)
Dataframe['var'] = Dataframe['var'].replace(0, 10)
Dataframe = Dataframe.astype(float)

# Generate sample data
X = np.array(np.log(Dataframe['var'])).reshape(-1, 1)

hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=3)
hdbscan_model.fit(X)
clusters = hdbscan_model.labels_
plt.scatter(X, np.zeros_like(X), c=clusters, cmap='viridis')
plt.show()
Dataframe['HDBSCAN'] = clusters

gmm = GaussianMixture(n_components=3)
gmm.fit(X)
labels = gmm.predict(X)
plt.scatter(X, np.zeros_like(X), c=labels, cmap='viridis')
plt.show()
Dataframe['GMM'] = labels

# if var < 100 label it as immobility
# if var <10000 and var < 10000 label it as nonlocomotion
# if var > 10000 label it as locomotion



pellet_arr = sr.select_ROI(video_path='test_group2/test.mp4')
hydrogel_arr = sr.select_ROI(video_path='test_group2/test.mp4')

# label the dataframe
# need to be modified


Dataframe["cluster"] = Dataframe["var"].apply(lambda x: "immobility" if x < 100 else ("nonlocomotion" if x < 10000 else "locomotion"))
for i in range(len(Dataframe)):
    if Dataframe["var"][i] != 'locomotion':
            # get the coordinates of the nose 
            nose_x = Dataframe["nose_x"][i]
            nose_y = Dataframe["nose_y"][i]
            # check if the nose is in the pellet
            if sr.is_in_roi(nose_x, nose_y, pellet_arr):
                Dataframe["cluster"][i] = "eating"
            # check if the nose is in the hydrogel
            if sr.is_in_roi(nose_x, nose_y, hydrogel_arr):
                Dataframe["cluster"][i] = "drinking"
            if Dataframe["var"][i] == 'nonlocomotion' and Dataframe['var_priority'][i] > 0.7:
                Dataframe["cluster"][i] = "grooming"



# save the dataframe
Dataframe.to_csv("test_group2/test_clustered.csv", index=False)
# map the cluster labels to the videos
import cv2
cap = cv2.VideoCapture("test_group2/test_labeled.mp4")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
font = cv2.FONT_HERSHEY_SIMPLEX
text_color = (0, 0, 0)
text_size = 1
text_thickness = 2

# save the editted video 
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = cap.get(cv2.CAP_PROP_FPS)
output_video = cv2.VideoWriter('test_group2/out.mp4', fourcc, fps, (width, height))


frame_number = 0
while frame_number < len(Dataframe):
    ret, frame = cap.read()
    if ret:
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        print(frame_number)
        cv2.putText(frame, ('cluster: {}, var {}').format(
             Dataframe['cluster'][frame_number-1], round(Dataframe['var'][frame_number-1], 2)
             ), (10, 50), font, text_size, text_color, text_thickness)
        
        cv2.putText(frame, ('GMM Cluster: {}').format(Dataframe['GMM'][frame_number-1]), (10, 100), font, text_size, text_color, text_thickness)
        cv2.putText(frame, ('HDBSCAN Cluster: {}').format(Dataframe['HDBSCAN'][frame_number-1]), (10, 150), font, text_size, text_color, text_thickness)
        
        cv2.imshow('frame', frame)
        output_video.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break


cap.release()
output_video.release()
cv2.destroyAllWindows()

