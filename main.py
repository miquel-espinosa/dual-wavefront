import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable


from functions import get_plots, gradient_plot, read_file

start, goal, map, obstacles, dist_s, dist_g = read_file("input.txt")



dist_transform_s = ndimage.distance_transform_edt(dist_s)
dist_transform_g = ndimage.distance_transform_edt(dist_g)
max_value_s = np.max(dist_transform_s)
max_value_g = np.max(dist_transform_g)
dist_transform_s_obstacles = dist_transform_s+obstacles*max_value_s
dist_transform_g_obstacles = dist_transform_g+obstacles*max_value_g



# Define plots
fig, (ax_map, ax_dist_s, ax_dist_g) = get_plots()

# Map (black and white)
ax_map.imshow(map, cmap=plt.cm.gray, origin='lower')

ax_map.scatter(*start, c='r', s=200, edgecolors='black')
ax_map.annotate('START', xy=(start[0]-0.5,start[1]+0.5))
ax_map.scatter(*goal, c='lime', s=200, edgecolors='black')
ax_map.annotate('GOAL', xy=(goal[0]-0.5,goal[1]+0.5))


gradient_plot(fig,ax_dist_s,map,dist_transform_s,dist_transform_s_obstacles, start, 'r')
gradient_plot(fig,ax_dist_g,map,dist_transform_g,dist_transform_g_obstacles, goal, 'lime')

ax_map.axis('off')
ax_dist_s.axis('off')
ax_dist_g.axis('off')


plt.show()

