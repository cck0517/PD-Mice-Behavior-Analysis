import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def rolling_variance(Dataframe, window=90):
    body_parts = ['nose', 'left_ear', 'right_ear', 'neck', 'left_side', 'right_side', 'tail_base']
    rolling_df = Dataframe.rolling(window=window)
    var_list = []
    var_priority_list = []
    for i, rolled_df in enumerate(rolling_df):
        print(f"Rolling part {i}")
        var, var_priority = get_rolling_variance(rolled_df, body_parts, pcutoff=0.7)
        var_list.append(var)
        var_priority_list.append(var_priority/var)

    Dataframe["var"] = pd.Series(var_list)
    Dataframe["var_priority"] = pd.Series(var_priority_list)
    return Dataframe

def get_rolling_variance(Dataframe, body_parts, pcutoff=0.9):
    var = 0
    var_priority = 0
    for bp in body_parts:
        prob = Dataframe[['likelihood_'+bp]].values.squeeze()
        mask = prob < pcutoff
        temp_x = np.ma.array(
            Dataframe[[bp + "_x"]].values.squeeze(),
            mask=mask,
        )
        temp_y = np.ma.array(
            Dataframe[[bp + "_y"]].values.squeeze(),
            mask=mask,
        )
        var = var + np.var(temp_x) + np.var(temp_y)

        if bp == 'nose':
            var_priority = var_priority + np.var(temp_x) + np.var(temp_y)
        elif bp == 'left_ear':
            var_priority = var_priority + np.var(temp_x) + np.var(temp_y)
        elif bp == 'right_ear':
            var_priority = var_priority + np.var(temp_x) + np.var(temp_y)
        elif bp == 'neck':
            var_priority = var_priority + np.var(temp_x) + np.var(temp_y)
    return var, var_priority



# Load data
Dataframe = pd.read_csv("slight grooming_1720.csv")
# # set new column names and reset index
# new_column_names = Dataframe.iloc[:2].apply(lambda x: '_'.join(map(str, x)), axis=0).tolist()
# Dataframe = Dataframe.set_axis(new_column_names, axis=1)
# Dataframe = Dataframe.drop([0, 1], axis=0)
# Dataframe = Dataframe.reset_index(drop=True)
Dataframe = Dataframe.replace('--', 0)
Dataframe = Dataframe.astype(float)



Dataframe = rolling_variance(Dataframe, window=120)

'''
# convert inf to nan
Dataframe["var"] = Dataframe["var"].replace([np.inf, -np.inf], np.nan)
# fill na with neighboring values
Dataframe["var"] = Dataframe["var"].fillna('ffill')
Dataframe["var"] = Dataframe["var"].fillna('bfill')
'''




# if var < 100 label it as immobility
# if var <10000 and var < 1000 label it as nonlocomotion
# if var > 10000 label it as locomotion


# replace '--' with 0 
Dataframe["var"] = Dataframe["var"].replace("--", 0)
Dataframe["var"] = Dataframe["var"].astype(float)
Dataframe['var_priority'] = Dataframe['var_priority'].fillna(0)
# label the dataframe
Dataframe["cluster"] = Dataframe["var"].apply(lambda x: "immobility" if x < 100 else ("nonlocomotion" if x < 10000 else "locomotion"))
Dataframe["cluster_priority"] = Dataframe['var_priority'].apply(lambda x: "grooming" if x >0.7 else 'None')

# map the cluster labels to the videos
import cv2
cap = cv2.VideoCapture("1720.mp4")
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
font = cv2.FONT_HERSHEY_SIMPLEX
text_color = (0, 0, 0)
text_size = 1
text_thickness = 2

# save the editted video 
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = cap.get(cv2.CAP_PROP_FPS)
output_video = cv2.VideoWriter('out.mp4', fourcc, fps, (width, height))


frame_number = 0
while frame_number < len(Dataframe):
    ret, frame = cap.read()
    if ret:
        frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        print(frame_number)
        if Dataframe['cluster_priority'][frame_number-1] != 'None':
            cv2.putText(frame, 'cluster: {}, var {}'.format(Dataframe['cluster_priority'][frame_number-1], Dataframe['var_priority'][frame_number-1]), (10, 50), font, text_size, text_color, text_thickness)
        else:
            cv2.putText(frame, 'cluster: {}, var {}'.format(Dataframe['cluster'][frame_number-1], Dataframe['var_priority'][frame_number-1]), (10, 50), font, text_size, text_color, text_thickness)
        cv2.imshow('frame', frame)
        output_video.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        break


cap.release()
output_video.release()
cv2.destroyAllWindows()



