import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# load the data from a csv file
# each csv file contains the coordinates of the body parts of a single animal
# the csv files are generated by the DeepLabCut software
locomotion = pd.read_csv('locomotion_8.csv')
immobility = pd.read_csv('sleeping_945.csv')
nonlocomotion = pd.read_csv('nonlocomotion_150.csv')

fps = 30
width= 1280
height = 1024
time_interval = 1 / fps 

# window size for rolling mean 
window_size = 60 

# smooth categorical data with rolling mean
def rolling_categorical_features(data, window_size= 60):
    map = {'locomotion': 0, 'immobility': 1, 'nonlocomotion': 2}
    data = data.map(map)
    data = data.rolling(window_size, min_periods=1).apply(np.mean).shift(0).astype(int)
    # reverse map 
    map = {0: 'locomotion', 1: 'immobility', 2: 'nonlocomotion'}
    data = data.map(map)
    return data

# smooth numerical data of features with rolling mean
def rolling_features(data, window_size= 60):
        return data.rolling(window_size, min_periods=1).mean().shift(0)

# calculate kinematic features for a single coordinate (x or y) for a single csv file
def dataset(data, coordinate='x', behavior=None):
    
    head_centroid = data[['nose_'+coordinate, 'left_ear_'+coordinate, 'right_ear_'+coordinate, 'neck_'+coordinate]].mean(axis=1)
    head_centroid = rolling_features(head_centroid)

    body_centroid = data[['neck_'+coordinate, 'left_side_'+coordinate, 'right_side_'+coordinate, 'tail_base_'+coordinate]].mean(axis=1)
    body_centroid = rolling_features(body_centroid)


    head_velocity = (head_centroid.diff() / time_interval).fillna(np.mean(head_centroid.diff() / time_interval))
    head_velocity = rolling_features(head_velocity)

    body_velocity = (body_centroid.diff() / time_interval).fillna(np.mean(body_centroid.diff() / time_interval))
    body_velocity = rolling_features(body_velocity)

    head_acceleration = (head_velocity.diff() / time_interval).fillna(np.mean(head_velocity.diff() / time_interval))
    head_acceleration = rolling_features(head_acceleration)

    body_acceleration = (body_velocity.diff() / time_interval).fillna(np.mean(body_velocity.diff() / time_interval))
    body_acceleration = rolling_features(body_acceleration)

    body_acceleration_squared = body_acceleration ** 2
    body_acceleration_squared = rolling_features(body_acceleration_squared)
    head_acceleration_squared = head_acceleration ** 2
    head_acceleration_squared = rolling_features(head_acceleration_squared)

    # make a dataframe
    df = pd.DataFrame({'head_centroid_'+coordinate: head_centroid, 
                       'body_centroid_'+coordinate: body_centroid, 
                       'head_velocity_'+coordinate: head_velocity, 
                       'body_velocity_'+coordinate: body_velocity, 
                       'head_acceleration_'+coordinate: head_acceleration, 
                       'body_acceleration_'+coordinate: body_acceleration, 
                       'body_acceleration_squared_'+coordinate: body_acceleration_squared,
                       'head_acceleration_squared_'+coordinate: head_acceleration_squared})
    
    if behavior:
        df['behavior'] = pd.Series([behavior]*len(df))
        df['behavior'] = rolling_categorical_features(df['behavior'])
    return df 

# compute kinematic features for x coordinate and y coordinate respectively and merge them into a single dataframe
def merge_data(data, behavior=None):
    x = dataset(data, coordinate='x', behavior=None)
    y = dataset(data, coordinate='y', behavior=behavior)
    df = x.merge(y, left_index=True, right_index=True)
    return df

# compute kinematic features for all csv files and concatenate them into a single dataframe
locomotion_df = merge_data(locomotion, behavior='locomotion')
immobility_df = merge_data(immobility, behavior='immobility')
nonlocomotion_df = merge_data(nonlocomotion, behavior='nonlocomotion')
df = pd.concat([locomotion_df, immobility_df, nonlocomotion_df])

# save the dataframe to a csv file
df.to_csv('kinematic_features.csv', index=False)

# split the dataframe into features and labels
X = df.iloc[:, :-1] # numerical features
y = df.iloc[:, -1] # categorical feature

print(y.value_counts())
# nonlocomotion    320
# immobility       268
# locomotion       200

######################### OLS ############################
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit the multinomial logistic regression model
model = LogisticRegression(multi_class='multinomial', solver='lbfgs')
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate the model performance
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print("Accuracy: ", accuracy)
# print("Classification report: \n", report)

# Use the model to predict new data
short = pd.read_csv('short_video.csv')
X_test = merge_data(short, behavior=None)
# Make predictions on the testing set
y_pred = model.predict(X_test)

######################### PCA ############################
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X_scaled)
color = {'locomotion': 'r', 'immobility': 'b', 'nonlocomotion': 'g'}
y = y.map(color)
# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_pca[:,0], X_pca[:,1], X_pca[:,2], color=y)
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
# plt.show()


######################### UMAP ############################
# TODO: try to plot the 3D UMAP and use HDBSCAN to cluster the data
import umap.umap_ as umap
reducer = umap.UMAP()
X_umap = reducer.fit_transform(X_scaled) #UMAP embedding
# Create a 2D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(X_umap[:,0], X_umap[:,1], color=y)
ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
# plt.show()
# Use HDBSCAN to cluster the data
import hdbscan
umap_embeddings = X_umap 
clusterer = hdbscan.HDBSCAN(min_cluster_size=3, gen_min_span_tree=True)
cluster_labels = clusterer.fit_predict(umap_embeddings)
cluster_labels = clusterer.fit_predict(umap_embeddings)
plt.scatter(umap_embeddings[:, 0], umap_embeddings[:, 1], c=cluster_labels, s=10, cmap='Spectral')
# plt.show()


