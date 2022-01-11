import numpy as np

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
                    start = [i,j]
                    dist_s[i][j] = 0
                if char == 'g':
                    goal = [i,j]
                    dist_g[i][j] = 0
                if char == 'o': # If obstacle
                    map[i][j] = 0
                    obstacles[i][j] = 1

    return start, goal, map, obstacles, dist_s, dist_g
