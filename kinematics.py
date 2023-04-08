import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# filter outlier points
def filter_outlier(Dataframe, window, pcutoff):
    body_parts = ['nose', 'leftear', 'rightear', 'neck', 'leftside', 'rightside', 'tailbase']
    # set new column names and reset index
    new_column_names = Dataframe.iloc[:2].apply(lambda x: '_'.join(map(str, x)), axis=0).tolist()
    Dataframe = Dataframe.set_axis(new_column_names, axis=1)
    Dataframe = Dataframe.drop([0, 1], axis=0)
    Dataframe = Dataframe.reset_index(drop=True).astype(float)

    for bp in body_parts:
        outliers = Dataframe[Dataframe[bp + "_likelihood"] < pcutoff]
        Dataframe.loc[outliers.index, bp + "_x"] = float('nan')
        Dataframe.loc[outliers.index, bp + "_y"] = float('nan')
        # fill outlier points with previous value if previous value is not outlier
        # fill outlier points with next value if next value is not outlier
        # fill outlier points with mean value if both previous and next values are outlier
        Dataframe[[bp + "_x"]] = Dataframe[[bp + "_x"]].fillna(method='ffill').fillna(method='bfill')
        Dataframe[[bp + "_y"]] = Dataframe[[bp + "_y"]].fillna(method='ffill').fillna(method='bfill')
    return Dataframe


# angular change
def interior_angle(p0, p1, p2):
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)
    angle = np.math.atan2(np.linalg.det([v0,v1]), np.dot(v0,v1))
    return np.degrees(angle)

def angle(Dataframe, window=90):
    angle_right = []

    for i in range(len(Dataframe)):
        p0 = [Dataframe['rightear_x'][i], Dataframe['rightear_y'][i]]
        p1 = [Dataframe['neck_x'][i], Dataframe['neck_y'][i]]
        p2 = [Dataframe['rightside_x'][i], Dataframe['rightside_y'][i]]
        angle = interior_angle(p0, p1, p2)
        angle_right.append(angle)
    angle_right = pd.Series(angle_right).rolling(window).mean()
    angle_right = angle_right.fillna(method='ffill')

    angle_left = []

    for i in range(len(Dataframe)):
        p0 = [Dataframe['leftear_x'][i], Dataframe['leftear_y'][i]]
        p1 = [Dataframe['neck_x'][i], Dataframe['neck_y'][i]]
        p2 = [Dataframe['leftside_x'][i], Dataframe['leftside_y'][i]]
        angle = interior_angle(p0, p1, p2)
        angle_left.append(angle)
    angle_left = pd.Series(angle_left).rolling(window).mean()
    angle_left = angle_left.fillna(method='ffill').fillna(method='bfill')

    assert len(angle_right) == len(angle_left) == len(Dataframe)

    return angle_right, angle_left


def angle_velocity(Dataframe, window=90):
    angle_right, angle_left = angle(Dataframe, window=window)
    angle_right_diff = np.diff(angle_right)
    angle_left_diff = np.diff(angle_left)
    angle_diff = [np.linalg.norm([angle_right_diff[i], angle_left_diff[i]]) for i in range(len(angle_right_diff))]
    angle_diff = np.array(angle_diff)
    angle_diff = np.hstack((angle_diff[0], angle_diff))
    velocity = pd.Series(angle_diff).rolling(window).apply(
        lambda x: x[window-1] - x[0], raw=True)
    velocity = velocity.fillna(method='ffill').fillna(method='bfill')
    period = 1/30*window
    velocity = np.abs(velocity/period)
    assert len(velocity) == len(Dataframe)
    return velocity


def angle_acceleration(Dataframe, window=90):
    velocity = angle_velocity(Dataframe, window=window)
    angle_velocity_diff = np.diff(velocity)
    angle_velocity_diff = np.hstack((angle_velocity_diff[0], angle_velocity_diff))
    acceleration = pd.Series(angle_velocity_diff).rolling(window).apply(
        lambda x: x[window-1] - x[0], raw=True)
    acceleration = acceleration.fillna(method='ffill').fillna(method='bfill')
    period = 1/30*window
    acceleration = acceleration/period
    assert len(acceleration) == len(Dataframe)
    return acceleration

# velocity
def velocity(Dataframe, body_parts, window=90):
    # body_parts = ['nose', 'leftear', 'rightear', 'neck', 'tailbase']
    body_parts = [bp + '_x' for bp in body_parts] + [bp + '_y' for bp in body_parts]
    position_x = Dataframe[body_parts].mean(axis=1)
    position_y = Dataframe[body_parts].mean(axis=1)
    position_diff_x = np.diff(position_x)
    position_diff_y = np.diff(position_y)
    position_diff = [np.linalg.norm([position_diff_x[i], position_diff_y[i]]) for i in range(len(position_diff_x))]
    position_diff = np.array(position_diff)
    position_diff = np.hstack((position_diff[0], position_diff))
    velocity = pd.Series(position_diff).rolling(window).apply(
        lambda x: x[window-1] - x[0], raw=True)
    velocity= velocity.fillna(method='ffill').fillna(method='bfill')
    period = 1/30*window 
    velocity = np.abs(velocity/period)
    assert len(velocity) == len(Dataframe)
    return velocity

# acceleration
def acceleration(Dataframe, body_parts, window=90):
    velocity_computed = velocity(Dataframe, body_parts, window=window)
    acceleration= np.diff(velocity_computed)
    acceleration = np.hstack((acceleration[0], acceleration))
    acceleration = pd.Series(acceleration).rolling(window).apply(
        lambda x: x[window-1] - x[0], raw=True)
    acceleration = acceleration.fillna(method='ffill').fillna(method='bfill')
    period = 1/30*window
    acceleration = acceleration/period
    assert len(acceleration) == len(Dataframe)
    return acceleration


def main(Dataframe, window=90,  body_parts = ['nose', 'leftear', 'rightear', 'neck', 'tailbase']):
    Dataframe = filter_outlier(Dataframe, window=90, pcutoff=0.7)
    head_body_angle_right, head_body_angle_left = angle(Dataframe)
    Dataframe['angle_right'] = head_body_angle_right
    Dataframe['angle_left'] = head_body_angle_left
    Dataframe['angle_velocity'] = angle_velocity(Dataframe, window=window)
    Dataframe['angle_acceleration'] = angle_acceleration(Dataframe, window=window)
    Dataframe['velocity'] = velocity(Dataframe, body_parts=body_parts, window=window)
    Dataframe['acceleration'] = acceleration(Dataframe, body_parts=body_parts, window=window)
    return Dataframe


def plot(Dataframe):
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(611)
    ax2 = fig.add_subplot(612)
    ax3 = fig.add_subplot(613)
    ax4 = fig.add_subplot(614)
    ax5 = fig.add_subplot(615)
    ax6 = fig.add_subplot(616)
    sns.lineplot(x=Dataframe.index, y=Dataframe['angle_right'], ax=ax1)
    sns.lineplot(x=Dataframe.index, y=Dataframe['angle_left'], ax=ax2)
    sns.lineplot(x=Dataframe.index, y=Dataframe['angle_velocity'], ax=ax3)
    sns.lineplot(x=Dataframe.index, y=Dataframe['angle_acceleration'], ax=ax4)
    sns.lineplot(x=Dataframe.index, y=Dataframe['velocity'], ax=ax5)
    sns.lineplot(x=Dataframe.index, y=Dataframe['acceleration'], ax=ax6)
    # align y labels position
    fig.align_ylabels()
    # align x axis position
    axes = [ax1, ax2, ax3, ax4, ax5, ax6]
    for ax in axes:
        ax.set_xlim(0, len(Dataframe))
    plt.show()


############################################################################################################

df_path = "C:\\Users\\chang\\DeepLabCut\\main\\JUPYTER\\DLC_Data\\videos\\2022-10-12 14-41-54DLC_resnet50_mainDec6shuffle1_120000.csv"

# angle is always computed for the ear, neck, and tailbase
# body parts included to calculate velocity and acceleration

body_parts = ['nose', 'leftear', 'rightear', 'neck', 'tailbase']

############################################################################################################

Dataframe = pd.read_csv(df_path)
Dataframe = main(Dataframe, window=90, body_parts = body_parts)
plot(Dataframe)
