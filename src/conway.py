import numpy as np


from colors import *
from constants import HUMAN, GIANT

def get_num_alive(cells, r, c, species):
    m, n = cells.shape
    sum_alive = 0
    
    for i in range(max(0, r - 1), min(m, r + 2)):
        for j in range(max(0, c - 1), min(n, c + 2)):
            if i == r and j == c and cells[i, j] == species:
                sum_alive -= 1
            if cells[i, j] == species:
                sum_alive += 1

    return sum_alive


def update(cells):
    nxt = np.zeros((cells.shape[0], cells.shape[1]))
    color_map = np.zeros((cells.shape[0], cells.shape[1], 3))

    for r, c in np.ndindex(cells.shape):

        species = cells[r, c]

        num_human = 0
        num_giant = 0
        
        if species == HUMAN:
            num_giant = get_num_alive(cells, r, c, GIANT)
        if species == GIANT:
            num_human = get_num_alive(cells, r, c, HUMAN)


        if species == HUMAN and num_human > 3:
            color_map[r, c] = background
        if species == HUMAN and num_giant > 1:
            color_map[r, c] = background

        if species == GIANT and num_giant > 2:
            color_map[r, c] = background
        if species == GIANT and num_human:
            color_map[r, c] = background
        
        if species == 0 and num_human > num_giant:
            nxt[r, c] = HUMAN if num_human > 2 else 0
            color_map[r, c] = human_alive
        else:
            nxt[r, c] = GIANT if num_giant > 3 else 0
            color_map[r, c] = giant_alive

        # color_map[r, c] = color_map[r, c] if cells[r, c] == 1 else background

    return nxt, color_map

def init(dimx, dimy, pattern):
    cells = np.zeros((dimy, dimx))
    
    pos = (3,3)
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells