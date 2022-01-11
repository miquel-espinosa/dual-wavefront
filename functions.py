import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable

def read_file(txt):
    with open(txt) as file:
        dims = [int(i) for i in file.readline().split("x")]
        obstacles = np.zeros((dims[0],dims[1]))
        map = np.ones((dims[0],dims[1]))
        dist_s = np.ones((dims[0],dims[1]))
        dist_g = np.ones((dims[0],dims[1]))
        
        lines = file.readlines()
        lines = list(reversed(lines))
        

        for i in range(dims[0]):
            for j in range(dims[1]):
                char = lines[i][j]
                reversed_char = lines[i][j]
                if char == 's':
                    start = [j,i]
                    dist_s[i][j] = 0
                if char == 'g':
                    goal = [j,i]
                    dist_g[i][j] = 0
                if char == 'o': # If obstacle
                    map[i][j] = 0
                    obstacles[i][j] = 1

    return start, goal, map, obstacles, dist_s, dist_g


def get_screen_dimensions():
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-zoomed', True)
    root.state('iconic')
    geometry = root.winfo_geometry()
    dpi = root.winfo_fpixels('1i')
    root.destroy()
    width = int(geometry.split('x')[0])
    height = int(geometry.split('x')[1].split('+')[0])
    return width/dpi, height/dpi



def get_plots():
    
    fig, axd = plt.subplot_mosaic([['ax_map', 'ax_dist_s'],
                               ['ax_map', 'ax_dist_g']])
    
    fig.tight_layout()

    fig.subplots_adjust(bottom=0.03, top=0.97, left=0.03, right=0.97)
    fig.subplots_adjust(wspace=0.1, hspace=0.1)

    width_in, height_in = get_screen_dimensions()
    fig.set_size_inches(round(width_in)-1,round(height_in)-1)

    return fig, (axd['ax_map'], axd['ax_dist_s'], axd['ax_dist_g'])

def gradient_plot(fig, ax_dist, map, dist_transform, dist_transform_obstacles, point, color):
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


    yd, xd = np.gradient(dist_transform)

    def func_to_vectorize(x, y, dx, dy, map, ax_dist, scaling=0.2):
        ax_dist.arrow(x, y, dx*scaling*map, dy*scaling*map, fc="k", ec="k", head_width=0.12, head_length=0.2)

    vectorized_arrow_drawing = np.vectorize(func_to_vectorize)

    vectorized_arrow_drawing(xv, yv, xd, yd, map, ax_dist, 0.2)

    divider = make_axes_locatable(ax_dist)
    cax = divider.append_axes('right', size='5%', pad=0.05)

    im = ax_dist.imshow(np.flip(dist_transform_obstacles,0), extent=[horizontal_min, horizontal_max, vertical_min, vertical_max])

    ax_dist.scatter(point[0]+0.5,point[1]+0.5, c=color, s=200, zorder=100, edgecolors='black')


    fig.colorbar(im, cax=cax, orientation='vertical')