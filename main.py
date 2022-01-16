import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import numpy as np
from scipy import ndimage
from functions import add_line, eucl_dist, get_best, get_plots, gradient_plot, read_file, circle_around, get_valid_point, hexcolor, add_video, neighbors, add_dot
import copy
from node import Node
from constants import ANIMATION, GRADIENT_PLOTS, INPUT_FILE_NAME, VIDEO, VIDEO_NAME

start, goal, map, obstacles, dist_s, dist_g = read_file(INPUT_FILE_NAME)

width = len(map[0])
height = len(map)

dist_transform_s = ndimage.distance_transform_edt(dist_s)
dist_transform_g = ndimage.distance_transform_edt(dist_g)
max_value_s = np.max(dist_transform_s)
max_value_g = np.max(dist_transform_g)
dist_transform_s_obstacles = dist_transform_s+obstacles*-max_value_s
dist_transform_g_obstacles = dist_transform_g+obstacles*-max_value_g



# Define plots
if GRADIENT_PLOTS: fig, (ax_map, ax_dist_s, ax_dist_g) = get_plots()
else: fig, ax_map = get_plots()

# Map (black and white)
ax_map.imshow(map, cmap=plt.cm.gray, origin='lower')

ax_map.scatter(*start, c='r', s=200, edgecolors='black')
ax_map.annotate('START', xy=(start[0]-0.5,start[1]+0.5))
ax_map.scatter(*goal, c='lime', s=200, edgecolors='black')
ax_map.annotate('GOAL', xy=(goal[0]-0.5,goal[1]+0.5))

if GRADIENT_PLOTS:
    gradient_plot(fig,ax_dist_s,map,dist_transform_s,dist_transform_s_obstacles, start, 'r', width, height)
    gradient_plot(fig,ax_dist_g,map,dist_transform_g,dist_transform_g_obstacles, goal, 'lime', width, height)

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
    video = add_video(width_video,height_video,VIDEO_NAME)


root_s = Node(xy=tuple(start), root=True)
root_g = Node(xy=tuple(goal), root=True)
queue_s = [root_s]
queue_g = [root_g]
intersect_point = None

while not meet:
    current_s = queue_s.pop(0) # Extract first element
    current_g = queue_g.pop(0) # Extract first element

    children_s = neighbors(map, root_s, current_s ,width, height)
    children_g = neighbors(map, root_g, current_g ,width, height)

    for node in children_s:
        current_s.add_son(node)
        queue_s.append(node)

    for node in children_g:
        current_g.add_son(node)
        queue_g.append(node)

    # Check exiting condition
    if root_s.find(current_g.xy):
        intersect_point = current_g.xy
        meet = True
    if root_g.find(current_s.xy):
        intersect_point = current_s.xy
        meet = True

    # Render colors and graphics
    max_distance = eucl_dist((0,0),(int(height/2),int(width/2)))
    color_s = hexcolor(eucl_dist(current_s.xy,start), max_distance)
    color_g = hexcolor(eucl_dist(current_g.xy,goal), max_distance, reverse=True)

    ax_map.add_artist(Rectangle(xy=(current_s.xy[0]-0.5,current_s.xy[1]-0.5), color=color_s, alpha=0.6, width=1, height=1))
    ax_map.add_artist(Rectangle(xy=(current_g.xy[0]-0.5,current_g.xy[1]-0.5), color=color_g, alpha=0.6, width=1, height=1))

    if ANIMATION:
        plt.pause(0.001)
        
    if VIDEO:
        string = fig.canvas.tostring_argb() # Extract the image as an ARGB string
        video.stdin.write(string) # Write to pipe

ax_map.add_artist(Rectangle(xy=(intersect_point[0]-0.5,intersect_point[1]-0.5), color='yellow', alpha=0.8, width=1, height=1, ec='k', lw=2))
ax_map.add_patch(add_dot(intersect_point))

if ANIMATION:
    plt.pause(0.001)

if VIDEO:
    string = fig.canvas.tostring_argb() # Extract the image as an ARGB string
    video.stdin.write(string) # Write to pipe


current_point_s = root_s.find(intersect_point)
current_point_g = root_g.find(intersect_point)
home_s = False
home_g = False


while not home_s or not home_g:
    if current_point_s.xy != tuple(start):
        ax_map.add_patch(add_line(current_point_s.xy,current_point_s.parent.xy))
        ax_map.add_patch(add_dot(current_point_s.parent.xy))
        ax_map.add_patch(add_dot(current_point_s.parent.xy))
        current_point_s = current_point_s.parent

    if current_point_g.xy != tuple(goal):
        ax_map.add_patch(add_line(current_point_g.xy,current_point_g.parent.xy))
        ax_map.add_patch(add_dot(current_point_g.parent.xy))
        current_point_g = current_point_g.parent

    home_s = (current_point_s.xy == tuple(start))
    home_g = (current_point_g.xy == tuple(goal))

    if ANIMATION:
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


plt.show(block=False)
plt.pause(3)
plt.close()