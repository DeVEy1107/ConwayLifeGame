import numpy as np
import pygame

from patterns import HUMAN_PATTERN, GIANT_PATTERN
from conway import data_update, init_pattern
from constants import HUMAN, GIANT, WALL


def pos2grid(pos, gridsize):
    '''
    將視窗中的座標位置轉換成二維陣列的索引位置
    '''
    x, y = pos
    r = y // gridsize
    c = x // gridsize 
    return r, c

class ConwayLifeGame:
    def __init__(self, rows, cols, gridsize):
        '''
        Args:
            - rows: 縱軸方向的網格數量
            - cols: 橫軸方向的網格數量
            - gridsize: 網格大小
        '''
        self.rows = rows
        self.cols = cols
        self.gridsize = gridsize

        self.load_image()

        self.screen = pygame.display.set_mode((rows * gridsize, cols * gridsize))
        
        self.clock = pygame.time.Clock()
        self.fps = 10 

        self.init_pattern()

        self.mousebtn_pressed = False # 紀錄滑鼠按鍵是否被按下

        self.is_running = True
        self.paused = False

        self.selected = HUMAN

        self.rumbling = False # 是否切換發動地鳴

    def load_image(self):
        '''
        載入圖片素材
        '''
        self.levi_img = pygame.transform.scale(
            pygame.image.load("images\Levi.png"), (self.gridsize, self.gridsize)
        )
        self.giant_img = pygame.transform.scale(
            pygame.image.load("images\giant.png"), (self.gridsize, self.gridsize)
        )
        self.grass_img = pygame.transform.scale(
            pygame.image.load("images\grass.png"), (self.gridsize, self.gridsize)
        )
        self.wall_img = pygame.transform.scale(
            pygame.image.load("images\wall.png"), (self.gridsize, self.gridsize)
        )

    def init_pattern(self):
        '''
        初始化網格資料中的布局內容
        '''
        self.grids = init_pattern(self.rows, self.cols, HUMAN_PATTERN, (0, 0))
        self.grids = init_pattern(self.rows, self.cols, GIANT_PATTERN, (15, 30), self.grids)

    def handle_events(self):
        '''
        處理按鍵互動事件
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    self.paused = not self.paused
                elif event.key == pygame.K_q:
                    self.is_running = False
                elif event.key == pygame.K_h:
                    self.selected = HUMAN
                elif event.key == pygame.K_g:
                    self.selected = GIANT
                elif event.key == pygame.K_w:
                    self.selected = WALL
                elif event.key == pygame.K_r:
                    self.rumbling  = not self.rumbling 
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousebtn_pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mousebtn_pressed = False
            if event.type == pygame.MOUSEMOTION and self.mousebtn_pressed:
                self.place_in_grid(event)

    def place_in_grid(self, event):
        '''
        放置選擇的人物並更新到網格資料中
        '''
        i, j = pos2grid(event.pos, self.gridsize)
        if self.paused and (0 <= i < self.cols and 0 <= j < self.rows):
            self.grids[i][j] = self.selected

            if self.selected == HUMAN and (self.grids[i, j] != GIANT or self.grids[i, j] != WALL):
                self.screen.blit(self.levi_img, (j * self.gridsize, i * self.gridsize))
            elif self.selected == GIANT and (self.grids[i, j] != HUMAN or self.grids[i, j] != WALL):
                self.screen.blit(self.giant_img, (j * self.gridsize, i * self.gridsize))
            elif self.selected == WALL and (self.grids[i, j] != HUMAN or self.grids[i, j] != GIANT):
                self.screen.blit(self.wall_img, (j * self.gridsize, i * self.gridsize))

            pygame.display.update()

    def update(self):
        '''
        將網格資料更新到視窗上
        '''
        for r, c in np.ndindex(self.grids.shape):
            self.screen.blit(self.grass_img, (c * self.gridsize, r * self.gridsize))
            if self.grids[r, c] == HUMAN:
                self.screen.blit(self.levi_img, (c * self.gridsize, r * self.gridsize))
            elif self.grids[r, c] == GIANT: 
                self.screen.blit(self.giant_img, (c * self.gridsize, r * self.gridsize))
            elif self.grids[r, c] == WALL:
                self.screen.blit(self.wall_img, (c * self.gridsize, r * self.gridsize))

        pygame.display.update()

    def run(self):
        '''
        開始執行遊戲
        '''
        while self.is_running:
            self.handle_events()

            if self.paused:
                # 暫停狀態
                self.update() 
                self.clock.tick(60)
            else:
                self.grids = data_update(self.grids, self.rumbling)
                self.update()
                self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__":
    game = ConwayLifeGame(50, 30, 25)
    game.run()

