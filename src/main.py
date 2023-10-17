import numpy as np
import pygame

from patterns import *
from conway import *
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

        self.levi_img = pygame.transform.scale(pygame.image.load("images\Levi.png"), (gridsize, gridsize))
        self.giant_img = pygame.transform.scale(pygame.image.load("images\giant.png"), (gridsize, gridsize))
        self.grass_img = pygame.transform.scale(pygame.image.load("images\grass.png"), (gridsize, gridsize))
        self.wall_img = pygame.transform.scale(pygame.image.load("images\wall.png"), (gridsize, gridsize))

        self.screen = pygame.display.set_mode((rows * gridsize, cols * gridsize))

        self.init_pattern()

        self.mousebtn_pressed = False 

        self.running = True
        self.paused = False

        self.selected = HUMAN

        self.rumbling = False

        self.clock = pygame.time.Clock()
        self.fps = 10

    def init_pattern(self):
        self.cells = init(self.rows, self.cols, HUMAN_PATTERN, (3, 3))
        # self.cells = init(self.rows, self.cols, BASE_PATTERN, (3, 3))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    self.paused = not self.paused
                elif event.key == pygame.K_q:
                    self.running = False
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
                self.drawCell(event)

    def switch_species(self):
        if self.paused:
            self.is_human = not self.is_human

    def drawCell(self, event):
        i, j = pos2grid(event.pos, self.gridsize)
        if self.paused:
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
        while self.running:
            self.handle_events()

            if self.paused:
                self.update() 
                self.clock.tick(60)
            else:
                self.cells = update(self.cells, self.rumbling)
                self.update()
                self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__":
    game = ConwayLifeGame(50, 30, 30)
    game.run()

