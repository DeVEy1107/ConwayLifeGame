import numpy as np
import pygame

from patterns import HUMAN_PATTERN, GIANT_PATTERN
from conway import data_update, init_pattern
from constants import HUMAN, GIANT, WALL


def pos2grid(pos, gridsize):
    x, y = pos
    r = y // gridsize
    c = x // gridsize 
    return r, c

class ConwayLifeGame:
    def __init__(self, rows, cols, gridsize):
        self.rows = rows
        self.cols = cols
        self.gridsize = gridsize

        self.load_image()

        self.screen = pygame.display.set_mode((rows * gridsize, cols * gridsize))

        self.init_pattern()

        self.mousebtn_pressed = False 

        self.is_running = True
        self.paused = False

        self.selected = HUMAN

        self.rumbling = False

        self.clock = pygame.time.Clock()
        self.fps = 10


    def load_image(self):
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
        self.cells = init_pattern(self.rows, self.cols, HUMAN_PATTERN, (0, 0))
        self.cells = init_pattern(self.rows, self.cols, GIANT_PATTERN, (30, 30), self.cells)

    def handle_events(self):
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
                self.draw_cell(event)

    def draw_cell(self, event):
        i, j = pos2grid(event.pos, self.gridsize)
        if self.paused and (0 <= i < self.cols and 0 <= j < self.rows):
            self.cells[i][j] = self.selected

            if self.selected == HUMAN and (self.cells[i, j] != GIANT or self.cells[i, j] != WALL):
                self.screen.blit(self.levi_img, (j * self.gridsize, i * self.gridsize))
            elif self.selected == GIANT and (self.cells[i, j] != HUMAN or self.cells[i, j] != WALL):
                self.screen.blit(self.giant_img, (j * self.gridsize, i * self.gridsize))
            elif self.selected == WALL and (self.cells[i, j] != HUMAN or self.cells[i, j] != GIANT):
                self.screen.blit(self.wall_img, (j * self.gridsize, i * self.gridsize))

            pygame.display.update()

    def update(self):
        for r, c in np.ndindex(self.cells.shape):
            self.screen.blit(self.grass_img, (c * self.gridsize, r * self.gridsize))
            if self.cells[r, c] == HUMAN:
                self.screen.blit(self.levi_img, (c * self.gridsize, r * self.gridsize))
            elif self.cells[r, c] == GIANT: 
                self.screen.blit(self.giant_img, (c * self.gridsize, r * self.gridsize))
            elif self.cells[r, c] == WALL:
                self.screen.blit(self.wall_img, (c * self.gridsize, r * self.gridsize))
        pygame.display.update()

    def run(self):
        while self.is_running:
            self.handle_events()

            if self.paused:
                self.update() 
                self.clock.tick(60)
            else:
                self.cells = data_update(self.cells, self.rumbling)
                self.update()
                self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__":
    game = ConwayLifeGame(80, 50, 15)
    game.run()

