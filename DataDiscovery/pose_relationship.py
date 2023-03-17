import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('kinematic_features.csv')


# plot histogram of each feature for each behavior
fig, ax = plt.subplots(3, 1, figsize=(5, 5))
loco = df[df['behavior'] == 'locomotion']['head_velocity_x']
immob = df[df['behavior'] == 'immobility']['head_velocity_x']
nonloco = df[df['behavior'] == 'nonlocomotion']['head_velocity_x']
sns.distplot(loco, ax=ax[0], color='red')
sns.distplot(immob, ax=ax[1], color='green')
sns.distplot(nonloco, ax=ax[2], color='blue')
ax.set_xlim([-200, 200])
plt.legend()
plt.show()

