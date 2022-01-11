import numpy as np
import tkinter as tk

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