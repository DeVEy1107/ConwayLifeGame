import numpy as np

from constants import HUMAN, GIANT, BACKGROUND, WALL

def get_num_alive(grids, r, c, species):
    '''
    取得目前網格周圍九宮格範圍內的物種數量

    Args:
        - grids: 二維陣列的網格資料
        - r: 當前網格的列索引
        - c: 當前網格的行索引
        - species: 物種
    '''
    m, n = grids.shape
    sum_alive = 0
    
    for i in range(max(0, r - 1), min(m, r + 2)):
        for j in range(max(0, c - 1), min(n, c + 2)): 
            if grids[i, j] == species:
                sum_alive += 1 
                if i == r and j == c:
                    sum_alive -= 1 

    return sum_alive

def data_update(grids, rumbling=False):
    '''
    更新網格資料至下一階段

    Args:
        - grids: 網格資料
        - rumbling: 是否發動地鳴
    '''

    # 更新至下一階段的網格資料
    nxt = np.zeros((grids.shape[0], grids.shape[1]))

    for r, c in np.ndindex(grids.shape):

        is_eaten = False

        if grids[r, c] == WALL:
            nxt[r, c] = WALL

        # 計算周圍的人類與巨人數量
        num_human = get_num_alive(grids, r, c, HUMAN)
        num_giant = get_num_alive(grids, r, c, GIANT)

        # 人類與巨人的互動關係
        if grids[r, c] == HUMAN and num_giant > 0:
            nxt[r, c] = BACKGROUND 
            is_eaten = True
        if grids[r, c] == GIANT and num_human > 1:
            nxt[r, c] = BACKGROUND
            is_eaten = True

        # 人類的康威生命遊戲模型
        if grids[r, c] == HUMAN and num_human < 2 or num_human > 3:
            nxt[r, c] = BACKGROUND
        elif (grids[r, c] == HUMAN and 2 <= num_human <= 3) or (grids[r, c] == BACKGROUND and num_human == 3):
            nxt[r, c] = BACKGROUND if is_eaten else HUMAN
    
        # 巨人的康威生命遊戲模型
        if rumbling:
            # 地鳴狀態
            if grids[r, c] == WALL:
                nxt[r, c] = GIANT

            if grids[r, c] == GIANT and num_giant < 1 or num_giant > 2:
                nxt[r, c] = BACKGROUND
            elif (grids[r, c] == GIANT and 1 <= num_giant <= 2) or (grids[r, c] == BACKGROUND and num_giant == 2):
                nxt[r, c] = BACKGROUND if is_eaten else GIANT
        else:
            # 一般狀態
            if grids[r, c] == GIANT and num_giant < 2 or num_giant > 3:
                nxt[r, c] = BACKGROUND
            elif (grids[r, c] == GIANT and 2 <= num_giant <= 3) or (grids[r, c] == BACKGROUND and num_giant == 3):
                nxt[r, c] = BACKGROUND if is_eaten else GIANT

    return nxt

def init_pattern(dimx, dimy, pattern, pos, grids=None):
    '''
    初始化網格資料中的布局內容
    '''
    if grids is None:
        grids = np.zeros((dimy, dimx))
    
    grids[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern

    return grids