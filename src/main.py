import numpy as np
import pygame

from colors import *
from patterns import *
from conway import *


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

        self.recording = False 

        self.running = True
        self.paused = False

        self.clock = pygame.time.Clock()
        self.fps = 60

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.recording = True
                self.mouse_positions = []  
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.recording = False
            elif event.type == pygame.MOUSEMOTION and self.recording:
                self.drawCell(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    self.paused = not self.paused
                elif event.key == pygame.K_q:
                    self.running = False

    def drawCell(self, event):
        i, j = pos2grid(event.pos, self.gridsize)
        if self.paused:
            self.cells[i][j] = 1
            self.color_map[i][j] = col_alive
            pygame.draw.rect(self.screen, col_alive, 
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
            else:
                self.cells, self.color_map = update(self.cells)
                self.update()

            self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__":
    game = ConwayLifeGame(80, 60, 12)
    game.run()

