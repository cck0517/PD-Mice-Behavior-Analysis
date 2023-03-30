import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings("ignore")

# Load data
df = pd.read_csv("test_full.csv")
pcutoff = 0.7
alphavalue = 0.5
colors = plt.cm.get_cmap("tab10", 7)




body_parts = ['nose', 'leftear', 'rightear', 'neck', 'leftside', 'rightside', 'tailbase']

rolling_df = df.rolling(window=90)
for i, Dataframe in enumerate(rolling_df):

    fig1 = plt.figure(figsize=(8, 6))
    ax1 = fig1.add_subplot(111, projection="3d")
    ax1.set_xlabel("X position in pixels")
    ax1.set_ylabel("Y position in pixels")
    ax1.set_zlabel("time")
    ax1.invert_yaxis()
    ax1.set_xlim([0, 1280])
    ax1.set_ylim([1024, 0])

    var_x = 0
    var_y = 0
    for bpindex, bp in enumerate(body_parts):
        prob = Dataframe[[bp+'_likelihood']].values.squeeze()
        
        mask = prob < pcutoff
        temp_x = np.ma.array(
            Dataframe[[bp + "_x"]].values.squeeze(),
            mask=mask,
        )
        temp_y = np.ma.array(
            Dataframe[[bp + "_y"]].values.squeeze(),
            mask=mask,
        )

        temp_t = np.ma.array(
            Dataframe[['frame']].values.squeeze(),
            mask=mask,
        )


        # calculate the variance of temp_x and temp_y
        var_x = var_x + np.var(temp_x)
        var_y = var_y + np.var(temp_y)

        ax1.plot(temp_x, temp_y, temp_t, color=colors(bpindex), alpha=alphavalue, label=bp)


    ax1.set_title('Trajectories variance: ' + str(var_x + var_y))
    plt.legend()
    plt.show()
