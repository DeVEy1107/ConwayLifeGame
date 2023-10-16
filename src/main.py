import numpy as np
import pygame

from colors import *
from patterns import *
from conway import *
from constants import HUMAN, GIANT

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

        self.screen = pygame.display.set_mode((rows * gridsize, cols * gridsize))

        self.cells = init(rows, cols, BASE_PATTERN)
        self.color_map = []

        self.mousebtn_pressed = False 

        self.running = True
        self.paused = False

        self.is_human = True

        self.clock = pygame.time.Clock()
        self.fps = 10

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    self.paused = not self.paused
                elif event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_s:
                    self.switch_species()

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
            draw_color = human_alive if self.is_human else giant_alive
            current_species = HUMAN if self.is_human else GIANT
            self.cells[i][j] = current_species
            self.color_map[i][j] = draw_color
            pygame.draw.rect(self.screen, draw_color, 
                            (j * self.gridsize, i * self.gridsize, self.gridsize-1, self.gridsize-1)
            )
            pygame.display.update()

    def update(self):
        for r, c in np.ndindex(self.cells.shape):
            pygame.draw.rect(self.screen, self.color_map[r, c], 
                             (c * self.gridsize, 
                              r * self.gridsize,
                              self.gridsize-1, self.gridsize-1)
            )
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()

            if self.paused:
                self.update() 
                self.clock.tick(60)
            else:
                self.cells, self.color_map = update(self.cells)
                self.update()

                self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__":
    game = ConwayLifeGame(80, 60, 12)
    game.run()

