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

        self.levi_img = pygame.transform.scale(pygame.image.load("images\Levi.png"), (gridsize, gridsize))
        self.giant_img = pygame.transform.scale(pygame.image.load("images\giant.png"), (gridsize, gridsize))
        self.grass_img = pygame.transform.scale(pygame.image.load("images\grass.png"), (gridsize, gridsize))

        self.init_pattern()
        self.color_map = []

        self.mousebtn_pressed = False 

        self.running = True
        self.paused = False

        self.is_human = True

        self.rumbling = False

        self.clock = pygame.time.Clock()
        self.fps = 10

    def init_pattern(self):
        # self.cells = init(self.rows, self.cols, HUMAN_PATTERN, (3, 3))
        # self.cells = init(self.rows, self.cols, GIANT_PATTERN, (20, 3), self.cells)
        self.cells = init(self.rows, self.cols, BASE_PATTERN, (3, 3))

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
                elif event.key == pygame.K_r:
                    self.rumbling  = not self.rumbling 
                elif event.key == pygame.K_a:
                    self.anti_shock = not self.anti_shock

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

            if self.is_human and self.cells[i][j] is not GIANT:
                self.screen.blit(self.levi_img, (j * self.gridsize, i * self.gridsize))
            elif not self.is_human and self.cells[i][j] is not HUMAN:
                self.screen.blit(self.giant_img, (j * self.gridsize, i * self.gridsize))

            # pygame.draw.rect(self.screen, draw_color, 
            #                 (j * self.gridsize, i * self.gridsize, self.gridsize-1, self.gridsize-1)
            # )

            pygame.display.update()

    def update(self):
        for r, c in np.ndindex(self.cells.shape):
            
            if self.cells[r, c] == 1:
                self.screen.blit(self.levi_img, (c * self.gridsize, r * self.gridsize))
            elif self.cells[r, c] == 2: 
                self.screen.blit(self.giant_img, (c * self.gridsize, r * self.gridsize))
            else:
                self.screen.blit(self.grass_img, (c * self.gridsize, r * self.gridsize))

                # pygame.draw.rect(self.screen, self.color_map[r, c], 
                #              (c * self.gridsize, 
                #               r * self.gridsize,
                #               self.gridsize, self.gridsize)
                # )

        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()

            if self.paused:
                self.update() 
                self.clock.tick(60)
            else:
                self.cells, self.color_map = update(self.cells, self.rumbling)
                self.update()

                self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__":
    game = ConwayLifeGame(30, 25, 50)
    game.run()

