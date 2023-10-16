import numpy as np


from colors import *
from constants import HUMAN, GIANT, BACKGROUND

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

def update(cells, rumbling=False):
    nxt = np.zeros((cells.shape[0], cells.shape[1]))
    color_map = np.zeros((cells.shape[0], cells.shape[1], 3))

    for r, c in np.ndindex(cells.shape):

        not_eaten = False

        num_human = get_num_alive(cells, r, c, HUMAN)
        num_giant = get_num_alive(cells, r, c, GIANT)


        if cells[r, c] == HUMAN and num_giant > 2:
            nxt[r, c] = GIANT
            color_map[r, c] = giant_alive
            not_eaten = True 
        if cells[r, c] == GIANT and num_human > 1:
            nxt[r, c] = HUMAN
            color_map[r, c] = human_alive 
            not_eaten = True 
        
        if cells[r, c] == HUMAN and num_human < 2 or num_human > 3:
            color_map[r, c] = human_about_to_die
            nxt[r, c] = BACKGROUND
        elif (cells[r, c] == HUMAN and 2 <= num_human <= 3) or (cells[r, c] == BACKGROUND and num_human == 3):
            if not_eaten:
                color_map[r, c] = human_alive
                nxt[r, c] = HUMAN
            else:
                color_map[r, c] = human_alive
                nxt[r, c] = HUMAN
            

        if rumbling:
            if cells[r, c] == GIANT and num_giant < 1 or num_giant > 2:
                color_map[r, c] = giant_about_to_die
                nxt[r, c] = BACKGROUND
            elif (cells[r, c] == GIANT and 1 <= num_giant <= 2) or (cells[r, c] == BACKGROUND and num_giant == 2):
                if not_eaten:
                    color_map[r, c] = giant_alive
                    nxt[r, c] = GIANT
                else:
                    color_map[r, c] = giant_alive
                    nxt[r, c] = GIANT
        else:
            if cells[r, c] == GIANT and num_giant < 2 or num_giant > 3:
                color_map[r, c] = giant_about_to_die
                nxt[r, c] = BACKGROUND
            elif (cells[r, c] == GIANT and 2 <= num_giant <= 3) or (cells[r, c] == BACKGROUND and num_giant == 3):
                if not_eaten:
                    color_map[r, c] = giant_alive
                    nxt[r, c] = GIANT
                else:
                    color_map[r, c] = giant_alive
                    nxt[r, c] = GIANT


        color_map[r, c] = color_map[r, c] if (cells[r, c] == HUMAN or cells[r, c] == GIANT) else background

    return nxt, color_map

def init(dimx, dimy, pattern, pos, cells=None):
    if cells is None:
        cells = np.zeros((dimy, dimx))
    
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells