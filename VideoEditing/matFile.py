import scipy.io as sio
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib_scalebar.scalebar import ScaleBar # pip install matplotlib-scalebar
current_path = os.getcwd()
spiketrain = sio.loadmat(current_path + '/VideoEditing/spiketrain.mat')
# get all unique values from the array
spike = spiketrain['spiketrain'] # spike is a 1D array
print(len(spike))
index = range(0, len(spike))

fig = plt.figure()
ax = fig.add_subplot(111)
#rolling window size
repeat_length = 3060
ax.set_xlim([0,repeat_length])
ax.set_ylim([0, 5])
line, = ax.plot([],[], c='black', lw=0.1)

# Create scale bar
scalebar = ScaleBar(dx=2, length_fraction=0.032, width_fraction=0.005, location='lower right', scale_formatter = lambda value, unit: f"{100} {'ms'}")         
ax.add_artist(scalebar)
# set x axis invisible
ax.get_xaxis().set_visible(False)

def animate(i):
    for f in range(i*51-51, i*51):
        print(f)
        if i == 0:
            continue
        if spike[f]>0:
            ax.plot([f,f],[1,5], c='black')
        if f>repeat_length:
            ax.set_xlim(f-repeat_length, f)
        else:
            ax.set_xlim(0,repeat_length)
    return line,

anim = FuncAnimation(fig, animate, frames=5520, interval=1, blit=False) # interval: delay between frames in milliseconds
# save the animation as mp4 video file
anim.save(current_path + '/VideoEditing/spiketrain_1.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
print('Done')
