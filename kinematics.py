import numpy as np
import pandas as pd

# df = pd.DataFrame({'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#                    'B': [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]})

# # Use rolling() method to roll the dataframe with a window of 90 rows
# rolling_df = df.rolling(window=3)

# rolling_df = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).rolling(window=3)
# # Loop through the rolling dataframe to get every rolling part
# for i, rolled_df in enumerate(rolling_df):
#     print(f"Rolling part {i}:")
#     print(rolled_df)



# angular change
def interior_angle(p0, p1, p2):
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)
    angle = np.math.atan2(np.linalg.det([v0,v1]), np.dot(v0,v1))
    return np.degrees(angle)

def angle(Dataframe, window=90):
    head_body_angle_right = []
    head_body_angle_left = []

    for i in range(len(Dataframe)):
        p0 = [Dataframe['rightear_x'][i], Dataframe['rightear_y'][i]]
        p1 = [Dataframe['neck_x'][i], Dataframe['neck_y'][i]]
        p2 = [Dataframe['rightside_x'][i], Dataframe['rightside_y'][i]]
        angle_right = interior_angle(p0, p1, p2)
        head_body_angle_right.append(angle_right)
    head_body_angle_right = pd.Series(head_body_angle_right).rolling(window).mean().shift(-int(window/2))
    head_body_angle_right = head_body_angle_right.fillna(method='ffill')
    head_body_angle_right = head_body_angle_right.fillna(method='bfill')

    for i in range(len(Dataframe)):
        p0 = [Dataframe['leftear_x'][i], Dataframe['leftear_y'][i]]
        p1 = [Dataframe['neck_x'][i], Dataframe['neck_y'][i]]
        p2 = [Dataframe['leftside_x'][i], Dataframe['leftside_y'][i]]
        angle_left = interior_angle(p0, p1, p2)
        head_body_angle_left.append(angle_left)
    head_body_angle_left = pd.Series(head_body_angle_left).rolling(window).mean().shift(-int(window/2))
    head_body_angle_left = head_body_angle_left.fillna(method='ffill')
    head_body_angle_left = head_body_angle_left.fillna(method='bfill')

    assert len(head_body_angle_right) == len(head_body_angle_left) == len(Dataframe)

    return head_body_angle_right, head_body_angle_left


# velocity
def velocity(Dataframe, window=90, min_periods=90):
    centroid_x = Dataframe[['nose_x', 'leftear_x', 'rightear_x', 'neck_x', 'tailbase_x']].mean(axis=1)
    centroid_y = Dataframe[['nose_y', 'leftear_y', 'rightear_y', 'neck_y', 'tailbase_y']].mean(axis=1)
    centroid_x_diff = np.diff(centroid_x)
    centroid_y_diff = np.diff(centroid_y)
    centroid = [np.linalg.norm([centroid_x_diff[i], centroid_y_diff[i]]) for i in range(len(centroid_x_diff))]
    centroid = np.array(centroid)
    centroid = np.hstack((centroid[0], centroid))
    centroid_velocity = pd.Series(centroid).rolling(window, min_periods).apply(
        lambda x: x[window-1] - x[0], raw=True).shift(-int(window/2))
    centroid_velocity= centroid_velocity.fillna(method='ffill', limit=min_periods).fillna(method='bfill', limit=min_periods)
    centroid_velocity = centroid_velocity/window
    assert len(centroid_velocity) == len(Dataframe)
    return centroid_velocity

# acceleration
def acceleration(Dataframe, window=90, min_periods=90):
    centroid_velocity = velocity(Dataframe, window=90, min_periods=90)
    centroid_acceleration= np.diff(centroid_velocity)
    centroid_acceleration = np.hstack((centroid_acceleration[0], centroid_acceleration))
    centroid_acceleration = pd.Series(centroid_acceleration).rolling(window, min_periods).apply(
        lambda x: x[window-1] - x[0], raw=True).shift(-int(window/2))
    centroid_acceleration = centroid_acceleration.fillna(method='ffill', limit=min_periods).fillna(method='bfill', limit=min_periods)
    centroid_acceleration = centroid_acceleration/window
    assert len(centroid_acceleration) == len(Dataframe)
    return centroid_acceleration


def main(Dataframe, window=90, min_periods=90):
    head_body_angle_right, head_body_angle_left = angle(Dataframe)
    centroid_velocity = velocity(Dataframe, window=90, min_periods=90)
    centroid_acceleration = acceleration(Dataframe, window=90, min_periods=90)
    Dataframe['head_body_angle_right'] = head_body_angle_right
    Dataframe['head_body_angle_left'] = head_body_angle_left
    Dataframe['centroid_velocity'] = centroid_velocity
    Dataframe['centroid_acceleration'] = centroid_acceleration
    return Dataframe


Dataframe = pd.read_csv("test.csv")

Dataframe = main(Dataframe)

# save to csv
Dataframe.to_csv("test_kinematics.csv", index=False)



# ######################### UMAP ############################
# X = main[['head_body_angle_right', 'head_body_angle_left', 
#                  'centroid_velocity', 'centroid_acceleration']]
# import umap.umap_ as umap
# import matplotlib.pyplot as plt
# reducer = umap.UMAP(n_components=3)
# X_umap = reducer.fit_transform(X) #UMAP embedding
# # Create a 3D scatter plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(X_umap[:,0], X_umap[:,1], X_umap[:, 2], alpha=0.5)
# ax.set_xlabel('UMAP1')
# ax.set_ylabel('UMAP2')
# ax.set_zlabel('UMAP3')
# plt.show()

# ######################### KNN ############################
# from sklearn.cluster import KMeans
# kmeans = KMeans(n_clusters=3, random_state=0).fit(X_umap)
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(X_umap[:,0], X_umap[:,1], X_umap[:, 2], c=kmeans.labels_, cmap='Spectral')
# ax.set_xlabel('UMAP1')
# ax.set_ylabel('UMAP2')
# ax.set_zlabel('UMAP3')
# plt.show()


