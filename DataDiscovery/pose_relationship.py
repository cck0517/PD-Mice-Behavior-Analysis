import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import numpy as np

df = pd.read_csv('kinematic_features.csv')


#################################################
# Plot kinematic distributions one by one 
#################################################
color_map = {'locomotion': 'red', 'immobility': 'green', 'nonlocomotion': 'blue'}
# extract numerical column names from the dataframe
numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns # len(numerical_columns) = 16
for col in numerical_columns:
    fig, ax = plt.subplots(3, 1, figsize=(5, 5), sharex=True)
    for i, behavior in enumerate(df['behavior'].unique()):
        sns.distplot(df[df['behavior'] == behavior][col], ax=ax[i], label=behavior, color=color_map[behavior])
        # if x axis is too large, use log scale
        ax[i].legend(loc="upper right")
        ax[i].set_ylabel('')
        if i == 1:
            ax[i].set_ylabel('Density')
    
plt.tight_layout()
plt.show()


#################################################
# Plot all the distributions in a single figure
#################################################

behavior = df['behavior'].unique()
fig11 = plt.figure(figsize=(10, 10), constrained_layout=False)

# gridspec inside gridspec
outer_grid = fig11.add_gridspec(4, 4, wspace=0.5, hspace=0.5)

for i in range(16):
    inner_grid = outer_grid[i].subgridspec(3, 1, wspace=0.5, hspace=0.2) 
    xmin = np.min(df[numerical_columns[i]])
    xmax = np.max(df[numerical_columns[i]])
    for j in range(3):
        ax = fig11.add_subplot(inner_grid[j])
        if xmax > 10000 or xmin < -10000:
            ax.set_xscale('log')
            sns.distplot(np.log(df[df['behavior'] == behavior[j]][numerical_columns[i]]), 
                     ax=ax, label=behavior[j], color=color_map[behavior[j]])
        else:
            sns.distplot(df[df['behavior'] == behavior[j]][numerical_columns[i]], 
                     ax=ax, label=behavior[j], color=color_map[behavior[j]])
        if xmin < 0:
            ax.set_xlim([xmin*1.1, xmax*1.1])
        else:
            ax.set_xlim([xmin*0.9, xmax*1.1])

        # set x axis label only for the bottom subplot
        ax.set_ylabel('')
        ax.set_xlabel('')
        if j == 2:
            if xmax > 10000 or xmin < -10000:
                ax.set_xlabel('log('+numerical_columns[i]+')')
            else:
                ax.set_xlabel(numerical_columns[i])
        if i==4 and j==1:
            ax.set_ylabel('Density', fontsize=15)
        # set legend only for the top right subplot
        if i == 3:
            ax.legend(loc="upper right", bbox_to_anchor=(1.5, 1))
            
fig11.suptitle('Distribution of kinematic features for each behavior', fontsize=15)

all_axes = fig11.get_axes()

# show only the outside spines
for ax in all_axes:
    for sp in ax.spines.values():
        sp.set_visible(True)
    if ax.is_first_row():
        ax.spines['top'].set_visible(True)
    if ax.is_last_row():
        ax.spines['bottom'].set_visible(True)
    if ax.is_first_col():
        ax.spines['left'].set_visible(True)
    if ax.is_last_col():
        ax.spines['right'].set_visible(True)
plt.show()
