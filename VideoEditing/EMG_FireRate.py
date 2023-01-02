import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
import os

# current path
current_path = os.getcwd()

# load data
df = pd.read_csv(current_path + '/VideoEditing/EMG_FireRate.csv', index_col=0) 
index = np.arange(0, len(df))
EMG = df.iloc[:, 0]
print(df.columns)
FireRate = df.loc[:, 'FireRate']


# create a figure 
fig = plt.figure()
# create two subplots
ax1 = fig.add_subplot(211) # 211 means 2 rows, 1 column, 1st subplot
ax2 = fig.add_subplot(212) # 212 means 2 rows, 1 column, 2nd subplot

# don't show the x axis
ax1.get_xaxis().set_visible(False)
ax2.get_xaxis().set_visible(False)

def animate(i):
    ax1.cla() # clear the previous image
    ax1.set_ylabel('Ampl.(µV)')
    ax1.plot(index[:i], EMG.head(i), c='black') # plot the line
    ax1.set_xlim([0, len(index)]) # fix the x axis
    ax1.set_ylim([0, 1.2*max(EMG)]) # fix the y axis

    ax2.cla() # clear the previous image
    ax2.set_ylabel('Spikes/s')
    ax2.plot(index[:i], FireRate.head(i), c='black') # plot the line
    ax2.set_xlim([0, len(index)]) # fix the x axis
    ax2.set_ylim([0, 1.2*max(FireRate)])# fix the y axis


# parameters: fig, animate, init_func, frames, interval, blit
# blit: whether to re-draw the entire figure each frame
# frames: number of frames to draw
# interval: delay between frames in milliseconds
anim = FuncAnimation(fig, animate, frames=len(df)+1, interval=1, blit=False) 
# save as mp4. This requires ffmpeg or mencoder to be installed
anim.save(current_path + '/VideoEditing/EMG_FireRate.mp4', fps=60, extra_args=['-vcodec', 'libx264'])
print("Done")


