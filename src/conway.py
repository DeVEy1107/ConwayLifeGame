import numpy as np

from constants import HUMAN, GIANT, BACKGROUND, WALL

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

    for r, c in np.ndindex(cells.shape):

        is_eaten = False

        if cells[r, c] == WALL:
            nxt[r, c] = WALL

        num_human = get_num_alive(cells, r, c, HUMAN)
        num_giant = get_num_alive(cells, r, c, GIANT)

        if cells[r, c] == HUMAN and num_giant > 0:
            nxt[r, c] = BACKGROUND
            is_eaten = True
        if cells[r, c] == GIANT and num_human > 1:
            nxt[r, c] = BACKGROUND
            is_eaten = True

        
        if cells[r, c] == HUMAN and num_human < 2 or num_human > 3:
            nxt[r, c] = BACKGROUND
        elif (cells[r, c] == HUMAN and 2 <= num_human <= 3) or (cells[r, c] == BACKGROUND and num_human == 3):
            nxt[r, c] = HUMAN
            if is_eaten:
                nxt[r, c] = BACKGROUND

        if rumbling:
            if cells[r, c] == WALL:
                nxt[r, c] = GIANT

            if cells[r, c] == GIANT and num_giant < 1 or num_giant > 2:
                nxt[r, c] = BACKGROUND
            elif (cells[r, c] == GIANT and 1 <= num_giant <= 2) or (cells[r, c] == BACKGROUND and num_giant == 2):
                nxt[r, c] = GIANT
                if is_eaten:
                    nxt[r, c] = BACKGROUND
        else:
            if cells[r, c] == GIANT and num_giant < 2 or num_giant > 3:
                nxt[r, c] = BACKGROUND
            elif (cells[r, c] == GIANT and 2 <= num_giant <= 3) or (cells[r, c] == BACKGROUND and num_giant == 3):
                nxt[r, c] = GIANT
                if is_eaten:
                    nxt[r, c] = BACKGROUND
                
    return nxt

def init(dimx, dimy, pattern, pos, cells=None):
    if cells is None:
        cells = np.zeros((dimy, dimx))
    
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells