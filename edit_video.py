import pandas as pd
import select_roi as sr
import numpy as np
import matplotlib.pyplot as plt
import hdbscan
from sklearn.mixture import GaussianMixture
import cv2

# load the dataframe
Dataframe = pd.read_csv("test_group2/test_kinematics.csv")
# replace '--' with 10
Dataframe = Dataframe.replace("--", 10)
Dataframe['var'] = Dataframe['var'].replace(0, 10)
Dataframe = Dataframe.astype(float)

# # Generate sample data
# X = np.array(np.log(Dataframe['var'])).reshape(-1, 1)

# hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=3)
# hdbscan_model.fit(X)
# clusters = hdbscan_model.labels_
# plt.scatter(X, np.zeros_like(X), c=clusters, cmap='viridis')
# plt.show()
# Dataframe['HDBSCAN'] = clusters

# gmm = GaussianMixture(n_components=3)
# gmm.fit(X)
# labels = gmm.predict(X)
# plt.scatter(X, np.zeros_like(X), c=labels, cmap='viridis')
# plt.show()
# Dataframe['GMM'] = labels

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
output_video = cv2.VideoWriter('test_group2/out_kinematics_v2.mp4', fourcc, fps, (width, height))

centroid_velocity = Dataframe['centroid_velocity']
centroid_acceleration = Dataframe['centroid_acceleration']
head_body_angle_left = Dataframe['head_body_angle_left']
head_body_angle_right = Dataframe['head_body_angle_right']

# 4 subplots
fig = plt.figure(figsize=(width/100, height/100), dpi=100)
ax1 = fig.add_subplot(411) 
ax2 = fig.add_subplot(412) 
ax3 = fig.add_subplot(413)
ax4 = fig.add_subplot(414)


canvas = fig.canvas

frame_number = 0
while frame_number < len(Dataframe):
    ret, frame = cap.read()
    if ret:
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        print(frame_number)
        cv2.putText(frame, ('cluster: {}, var {}').format(
             Dataframe['cluster'][frame_number-1], round(Dataframe['var'][frame_number-1], 2)
             ), (10, 50), font, text_size, text_color, text_thickness)
        
        # cv2.putText(frame, ('GMM Cluster: {}').format(Dataframe['GMM'][frame_number-1]), (10, 100), font, text_size, text_color, text_thickness)
        # cv2.putText(frame, ('HDBSCAN Cluster: {}').format(Dataframe['HDBSCAN'][frame_number-1]), (10, 150), font, text_size, text_color, text_thickness)


        velocity = centroid_velocity[0:frame_number]
        acceleration = centroid_acceleration[0:frame_number]
        angle_left = head_body_angle_left[0:frame_number]
        angle_right = head_body_angle_right[0:frame_number]
        x = np.arange(0, len(velocity))



        # Plot time series data
        ax1.plot(x, velocity, color='blue', linewidth=1, label='centroid_velocity')
        ax2.plot(x, acceleration, color='red', linewidth=1, label='centroid_acceleration')
        ax3.plot(x, angle_left, color='green', linewidth=1, label='head_body_angle_left')
        ax4.plot(x, angle_right, color='black', linewidth=1, label='head_body_angle_right')

        # set the y axis limit
        ax1.set_ylim(min(centroid_velocity), max(centroid_velocity))
        ax2.set_ylim(min(centroid_acceleration), max(centroid_acceleration))
        ax3.set_ylim(min(head_body_angle_left), max(head_body_angle_left))
        ax4.set_ylim(min(head_body_angle_right), max(head_body_angle_right))
    
        # set a rolling window to show the 1000 frames each time 
        ax1.set_xlim(max(0, frame_number-100), frame_number)
        ax2.set_xlim(max(0, frame_number-100), frame_number)
        ax3.set_xlim(max(0, frame_number-100), frame_number)
        ax4.set_xlim(max(0, frame_number-100), frame_number)

        ax1.set_xlabel('Frame Number')

        ax1.set_ylabel('Centroid Velocity')
        ax2.set_ylabel('Centroid Acceleration')
        ax3.set_ylabel('Head Body Angle Left')
        ax4.set_ylabel('Head Body Angle Right')

        ax1.grid(True)
        ax2.grid(True)
        ax3.grid(True)
        ax4.grid(True)


        # Convert plot to numpy array
        canvas.draw()
        plot_array = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
        plot_array = plot_array.reshape(canvas.get_width_height()[::-1] + (3,))
        plot_array = cv2.cvtColor(plot_array, cv2.COLOR_RGB2BGR)

        # Combine plot array with video frame
        combined = cv2.addWeighted(frame, 0.7, plot_array, 0.3, 0)

        
        
        # Display the combined image
        cv2.imshow('frame', combined)
        
        output_video.write(combined)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break


cap.release()
output_video.release()
cv2.destroyAllWindows()

