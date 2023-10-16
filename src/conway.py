import numpy as np

from colors import *

def update(cells):
    nxt = np.zeros((cells.shape[0], cells.shape[1]))
    color_map = np.zeros((cells.shape[0], cells.shape[1], 3))

    for r, c in np.ndindex(cells.shape):
        num_alive = np.sum(cells[r-1:r+2, c-1:c+2]) - cells[r, c]

        if cells[r, c] == 1 and num_alive < 2 or num_alive > 3:
            color_map[r, c] = col_about_to_die
        elif (cells[r, c] == 1 and 2 <= num_alive <= 3) or (cells[r, c] == 0 and num_alive == 3):
            color_map[r, c] = col_alive
            nxt[r, c] = 1

        color_map[r, c] = color_map[r, c] if cells[r, c] == 1 else col_background

    return nxt, color_map

def init(dimx, dimy, pattern):
    cells = np.zeros((dimy, dimx))
    
    pos = (3,3)
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells