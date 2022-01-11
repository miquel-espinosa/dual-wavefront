import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable


from functions import read_file

start, goal, map, obstacles, dist_s, dist_g = read_file("input.txt")



dist_transform_s = ndimage.distance_transform_edt(dist_s)
max_value = np.max(dist_transform_s)
dist_transform_s_obstacles = dist_transform_s+obstacles*max_value

# Define plots
fig, (ax_map, ax_dist) = plt.subplots(1,2)
fig.tight_layout()
# Map (black and white)
ax_map.imshow(map, cmap=plt.cm.gray, origin='lower')

fig.subplots_adjust(bottom=0.03, top=0.97, left=0.03, right=0.97)
fig.subplots_adjust(wspace=0.1, hspace=0.1)

horizontal_min, horizontal_max, horizontal_stepsize = 0, 23, 1
vertical_min, vertical_max, vertical_stepsize = 0, 10, 1

horizontal_dist = horizontal_max-horizontal_min
vertical_dist = vertical_max-vertical_min

horizontal_stepsize = horizontal_dist / float(math.ceil(horizontal_dist/float(horizontal_stepsize)))
vertical_stepsize = vertical_dist / float(math.ceil(vertical_dist/float(vertical_stepsize)))

xv, yv = np.meshgrid(np.arange(horizontal_min, horizontal_max, horizontal_stepsize),
                     np.arange(vertical_min, vertical_max, vertical_stepsize))

xv+=horizontal_stepsize/2.0
yv+=vertical_stepsize/2.0


yd, xd = np.gradient(dist_transform_s)

def func_to_vectorize(x, y, dx, dy, map, scaling=0.2):
    plt.arrow(x, y, dx*scaling*map, dy*scaling*map, fc="k", ec="k", head_width=0.12, head_length=0.2)

vectorized_arrow_drawing = np.vectorize(func_to_vectorize)

im = ax_dist.imshow(np.flip(dist_transform_s_obstacles,0), extent=[horizontal_min, horizontal_max, vertical_min, vertical_max])
vectorized_arrow_drawing(xv, yv, xd, yd, map, 0.2)

divider = make_axes_locatable(ax_dist)
cax = divider.append_axes('right', size='5%', pad=0.05)

fig.colorbar(im, cax=cax, orientation='vertical')



# img_dist = ax_dist.imshow(dist)

# cbar = fig.colorbar(img_dist, ax=ax_dist)

# ax_dist.axis('off')
plt.show()

