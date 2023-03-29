import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings("ignore")

# Load data
df = pd.read_csv("nonlocomotion_150.csv")
pcutoff = 0.7
alphavalue = 0.5
colors = plt.cm.get_cmap("tab10", 7)



body_parts = ['nose', 'left_ear', 'right_ear', 'neck', 'left_side', 'right_side', 'tail_base']

# rolling_df = df.rolling(window=90)
# for i, Dataframe in enumerate(rolling_df):

#     fig1 = plt.figure(figsize=(8, 6))
#     ax1 = fig1.add_subplot(111, projection="3d")
#     ax1.set_xlabel("X position in pixels")
#     ax1.set_ylabel("Y position in pixels")
#     ax1.set_zlabel("time")
#     ax1.invert_yaxis()
#     ax1.set_xlim([0, 1280])
#     ax1.set_ylim([1024, 0])

#     var_x = 0
#     var_y = 0
#     for bpindex, bp in enumerate(body_parts):
#         prob = Dataframe[['likelihood_' + bp]].values.squeeze()
        
#         mask = prob < pcutoff
#         temp_x = np.ma.array(
#             Dataframe[[bp + "_x"]].values.squeeze(),
#             mask=mask,
#         )
#         temp_y = np.ma.array(
#             Dataframe[[bp + "_y"]].values.squeeze(),
#             mask=mask,
#         )

#         temp_t = np.ma.array(
#             Dataframe[['frame']].values.squeeze(),
#             mask=mask,
#         )


#         # calculate the variance of temp_x and temp_y
#         var_x = var_x + np.var(temp_x)
#         var_y = var_y + np.var(temp_y)

#         ax1.plot(temp_x, temp_y, temp_t, color=colors(bpindex), alpha=alphavalue, label=bp)


#     ax1.set_title('nonlocomotion variance: ' + str(var_x + var_y))
#     plt.legend()
#     plt.show()


def rolling_variance(Dataframe, window=90):
    body_parts = ['nose', 'left_ear', 'right_ear', 'neck', 'left_side', 'right_side', 'tail_base']
    rolling_df = Dataframe.rolling(window=window)
    var_list = []
    for i, rolled_df in enumerate(rolling_df):
        print(f"Rolling part {i}:")
        var = get_rolling_variance(rolled_df, body_parts, pcutoff=0.5)
        var_list.append(var)
    Dataframe["var"] = pd.Series(var_list)
    return Dataframe

def get_rolling_variance(Dataframe, body_parts, pcutoff=0.5):
    var_x = 0
    var_y = 0
    for bp in body_parts:
        prob = Dataframe[['likelihood_' + bp]].values.squeeze()
        mask = prob < pcutoff
        temp_x = np.ma.array(
            Dataframe[[bp + "_x"]].values.squeeze(),
            mask=mask,
        )
        temp_y = np.ma.array(
            Dataframe[[bp + "_y"]].values.squeeze(),
            mask=mask,
        )
        var_x = var_x + np.var(temp_x)
        var_y = var_y + np.var(temp_y)
    return var_x+var_y



short_df = pd.read_csv("short_video.csv")
short_df = rolling_variance(short_df, window=90)

X = short_df['var'].values

######################### UMAP ############################
import umap.umap_ as umap
reducer = umap.UMAP(n_components=3)
X_umap = reducer.fit_transform(X) #UMAP embedding
# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_umap[:,0], X_umap[:,1], X_umap[:, 2], alpha=0.5)
ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
ax.set_zlabel('UMAP3')
plt.show()

# Use KNN to cluster the data
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=0).fit(X_umap)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_umap[:,0], X_umap[:,1], X_umap[:, 2], c=kmeans.labels_, cmap='Spectral')
ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
ax.set_zlabel('UMAP3')
plt.show()

# add the cluster labels to the dataframe
df['cluster'] = kmeans.labels_
# save the dataframe to a csv file
df.to_csv('clustered_kinematic_features.csv', index=False)

