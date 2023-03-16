import statsmodels as sm
import pandas as pd

locomotion = pd.read_csv('locomotion_8.csv')
immobility = pd.read_csv('sleeping_945.csv')
nonlocomotion = pd.read_csv('nonlocomotion_150.csv')

locomotion_df = sm.merge_data(locomotion, behavior='locomotion')
immobility_df = sm.merge_data(immobility, behavior='immobility')
nonlocomotion_df = sm.merge_data(nonlocomotion, behavior='nonlocomotion')
df = pd.concat([locomotion_df, immobility_df, nonlocomotion_df])

print(df.head())
print(nonlocomotion_df.columns)

# plot histogram of each feature for each behavior
# plot 4 histograms together 
# head_centroid_x, head_centroid_y, body_centroid_x, body_centroid_y
import matplotlib.pyplot as plt
import seaborn as sns
sns.histplot(data=locomotion_df, x='head_centroid_x',
                hue='behavior', bins=100,
                kde=True, stat='density', common_norm=False)
plt.legend()
plt.show()

