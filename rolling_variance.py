import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


def rolling_variance(Dataframe, window=90):
    body_parts = ['nose', 'leftear', 'rightear', 'neck', 'leftside', 'rightside', 'tailbase']
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

def get_rolling_variance(Dataframe, body_parts, pcutoff=0.7):
    var = 0
    var_priority = 0
    for bp in body_parts:
        prob = Dataframe[[bp + "_likelihood"]].values.squeeze()
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
        elif bp == 'leftear':
            var_priority = var_priority + np.var(temp_x) + np.var(temp_y)
        elif bp == 'rightear':
            var_priority = var_priority + np.var(temp_x) + np.var(temp_y)
        elif bp == 'neck':
            var_priority = var_priority + np.var(temp_x) + np.var(temp_y)
    return var, var_priority

# Load data
Dataframe = pd.read_csv("test/test.csv")
# set new column names and reset index
# new_column_names = Dataframe.iloc[:2].apply(lambda x: '_'.join(map(str, x)), axis=0).tolist()
# Dataframe = Dataframe.set_axis(new_column_names, axis=1)
# Dataframe = Dataframe.drop([0, 1], axis=0)
# Dataframe = Dataframe.reset_index(drop=True)
# Dataframe = Dataframe.replace('--', 0)
# Dataframe = Dataframe.astype(float)

body_parts = ['nose', 'leftear', 'rightear', 'neck', 'leftside', 'rightside', 'tailbase']

Dataframe = rolling_variance(Dataframe, window=120)

'''
# convert inf to nan
Dataframe["var"] = Dataframe["var"].replace([np.inf, -np.inf], np.nan)
# fill na with neighboring values
Dataframe["var"] = Dataframe["var"].fillna('ffill')
Dataframe["var"] = Dataframe["var"].fillna('bfill')
'''
# save the dataframe
Dataframe.to_csv("test/test.csv", index=False)
