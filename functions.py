from xml.dom import NO_DATA_ALLOWED_ERR
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import math
from mpl_toolkits.axes_grid1 import make_axes_locatable
import subprocess
import matplotlib.patches as Patch
from matplotlib.path import Path
from node import Node

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

def circle_around(x, y):
    r = 1
    i, j = x-1, y-1
    while True:
        while i < x+r:
            i += 1
            yield r, (i, j)
        while j < y+r:
            j += 1
            yield r, (i, j)
        while i > x-r:
            i -= 1
            yield r, (i, j)
        while j > y-r:
            j -= 1
            yield r, (i, j)
        r += 1
        j -= 1
        yield r, (i, j)

def get_valid_point(iter, obstacles, width, height):
    while True:
        point = next(iter)
        if point[1][0] < width and \
            point[1][1] < height and \
            point[1][0] >= 0 and \
            point[1][1] >= 0 and \
            obstacles[point[1][1]][point[1][0]] != 1:
            return point[1]
        # ax_map.scatter(point_s[1][0],point_s[1][1])
        # visited_s.append(point_s[1])


def add_video(canvas_width, canvas_height,name):
    outf = str(name+'.mp4')
    # Open an ffmpeg process
    cmdstring = ('ffmpeg', 
        '-y', '-r', '16', # overwrite, 30fps
        '-s', '%dx%d' % (canvas_width, canvas_height), # size of image string
        '-pix_fmt', 'argb', # format
        '-f', 'rawvideo',  '-i', '-', # tell ffmpeg to expect raw video from the pipe
        '-vb', '20000k',
        '-hide_banner','-loglevel','error',
        '-vcodec', 'libx264', outf) # output encoding
    return subprocess.Popen(cmdstring, stdin=subprocess.PIPE)

def eucl_dist(p1,p2):
    """ Scalar distance from p1 to p2 (without direction)"""
    return math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def hexcolor(value, reverse=False):
    if value <= 50:
        r = 255
        g = int(255*value/50)
        b = 0
    else:
        r = int(255*(100-value)/50)
        g = 255
        b = 0
    if reverse:
        r, g = g, r
    return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0") for c in (r, g, b)])

def neighbors(map, root, current, width, height):
    x = current.xy[0]
    y = current.xy[1]
    node_cost = current.cost
    neig = []
    for j in range(y-1,y+2):
        for i in range(x-1,x+2):
            if i >= 0 and i < width and j >= 0 and j < height: # Check inside bounds
                if (map[j][i] == 1) and (j!=y or i!=x): # Check if obstacle or itself
                    # if DIAGONALS:
                    if root.find((i,j)) == None: # If does not exist in current tree
                        neig.append(Node((i,j), cost=node_cost+1))
    return neig

def get_best(list_p,dist_p):
    min = 100000000000000
    best = None
    for p in list_p:
        new_dist = dist_p[p[1]][p[0]]
        if new_dist < min:
            min = new_dist
            best = p
    return best

def add_line(p1,p2):
    verts = [p1, p2]
    codes = [Path.MOVETO,Path.LINETO]
    path = Path(verts, codes)
    return Patch.PathPatch(path, color='black', lw=2, zorder=20)

def add_dot(p):
    return Patch.Circle(xy=p, radius=0.1, color='black', lw=2, zorder=20, alpha=0.75)