import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import numpy as np
from scipy import ndimage
from functions import add_line, eucl_dist, get_best, get_plots, gradient_plot, read_file, circle_around, get_valid_point, hexcolor, add_video, neighbors, add_dot
import time

VIDEO = False
ANIMATION = False

start, goal, map, obstacles, dist_s, dist_g = read_file("input.txt")

width = len(map[0])
height = len(map)

dist_transform_s = ndimage.distance_transform_edt(dist_s)
dist_transform_g = ndimage.distance_transform_edt(dist_g)
max_value_s = np.max(dist_transform_s)
max_value_g = np.max(dist_transform_g)
dist_transform_s_obstacles = dist_transform_s+obstacles*-max_value_s
dist_transform_g_obstacles = dist_transform_g+obstacles*-max_value_g



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

# ax_map.axis('off')
ax_dist_s.axis('off')
ax_dist_g.axis('off')

visited_s = [tuple(start)]
visited_g = [goal]

iter_s = circle_around(*start)
iter_g = circle_around(*goal)


meet = False

if VIDEO:
    win = fig.canvas.window()
    win.setFixedSize(win.size())
    width_video, height_video = fig.canvas.get_width_height()
    video = add_video(width_video,height_video,'video')


# dir_map_s = np.matrix(np.ones((width,height))*np.inf)
# dir_map_g = np.zeros_like(map)

while not meet:
    point_s = get_valid_point(iter_s, obstacles, width, height)
    point_g = get_valid_point(iter_g, obstacles, width, height)

    visited_s.append(point_s)
    visited_g.append(point_g)

    color_s = hexcolor(eucl_dist(point_s,start)*4)
    color_g = hexcolor(eucl_dist(point_s,start)*4, reverse=True)


    ax_map.add_artist(Rectangle(xy=(point_s[0]-0.5,point_s[1]-0.5), color=color_s, alpha=0.6, width=1, height=1))
    ax_map.add_artist(Rectangle(xy=(point_g[0]-0.5,point_g[1]-0.5), color=color_g, alpha=0.6, width=1, height=1))

    meet = point_s in visited_g or point_g in visited_s
    
    if ANIMATION:
        plt.pause(0.001)

    if VIDEO:
        string = fig.canvas.tostring_argb() # Extract the image as an ARGB string
        video.stdin.write(string) # Write to pipe

intersect_point = [e for e in visited_s if e in visited_g][0]
ax_map.add_artist(Rectangle(xy=(intersect_point[0]-0.5,intersect_point[1]-0.5), color='yellow', alpha=0.8, width=1, height=1, ec='k', lw=2))

plt.pause(0.001)

if VIDEO:
    string = fig.canvas.tostring_argb() # Extract the image as an ARGB string
    video.stdin.write(string) # Write to pipe


current_point_s = intersect_point
current_point_g = intersect_point
home_s = False
home_g = False


while not home_s or not home_g:
    if current_point_s != tuple(start):
        neig_s = neighbors(map,*current_point_s, width, height)
        best_s = get_best(neig_s,dist_transform_s_obstacles)
        ax_map.add_patch(add_line(current_point_s,best_s))
        ax_map.add_patch(add_dot(best_s))
        current_point_s = best_s

    if current_point_g != tuple(goal):
        neig_g = neighbors(map,*current_point_g, width, height)
        best_g = get_best(neig_g,dist_transform_g_obstacles)
        ax_map.add_patch(add_line(current_point_g,best_g))
        ax_map.add_patch(add_dot(best_g))
        current_point_g = best_g

    home_s = (best_s == tuple(start))
    home_g = (best_g == tuple(goal))

    plt.pause(0.001)

    if VIDEO:
        for _ in range(5):
            string = fig.canvas.tostring_argb() 
            video.stdin.write(string) 

    
if VIDEO:
    for _ in range(20):
        plt.pause(0.01)
        string = fig.canvas.tostring_argb() 
        video.stdin.write(string) 

    video.communicate()


plt.show()

