import numpy as np
import pygame

col_about_to_die = (200, 200, 225)
col_alive = (255, 255, 215)
col_background = (0, 10, 100)
col_grid = (30, 30, 60)

BASE_PATTERN = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                         [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

def update(screen, cells, cellsize):
    nxt = np.zeros((cells.shape[0], cells.shape[1]))
    color_map = np.zeros((cells.shape[0], cells.shape[1], 3))

    for r, c in np.ndindex(cells.shape):
        num_alive = np.sum(cells[r-1:r+2, c-1:c+2]) - cells[r, c]

        if cells[r, c] == 1 and num_alive < 2 or num_alive > 3:
            color_map[r, c] = col_about_to_die
        elif (cells[r, c] == 1 and 2 <= num_alive <= 3) or (cells[r, c] == 0 and num_alive == 3):
            color_map[r, c] = col_alive
            nxt[r, c] = 1

        color_map[r, c] = color_map[r, c] if cells[r, c] == 1 else col_background

    return nxt, color_map

def init(dimx, dimy, pattern):
    cells = np.zeros((dimy, dimx))
    
    pos = (3,3)
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells

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

        self.mouse_position = (0, 0)
        self.mouse_positions = []
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
                self.mouse_position = event.pos
                i, j = pos2grid(event.pos, self.gridsize)
                if self.paused:
                    self.cells[i][j] = 1
                    self.color_map[i][j] = col_alive
                    pygame.draw.rect(self.screen, col_alive, 
                                    (j * self.gridsize, i * self.gridsize, self.gridsize-1, self.gridsize-1)
                    )
                    pygame.display.update()
                self.mouse_positions.append(self.mouse_position)  
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    self.paused = not self.paused
                elif event.key == pygame.K_q:
                    self.running = False
            
    def update(self):
        for r, c in np.ndindex(self.cells.shape):
            pygame.draw.rect(self.screen, self.color_map[r, c], 
                             (c * self.gridsize, 
                              r * self.gridsize,
                              self.gridsize-1, self.gridsize-1)
            )

        pygame.display.update()
        pass

    def run(self):
        while self.running:
            self.handle_events()

            if self.paused:
                self.update()       
            else:
                self.cells, self.color_map = update(self.screen, self.cells, self.gridsize)
                self.update()

            self.clock.tick(self.fps)

        pygame.quit()

if __name__ == "__main__":
    game = ConwayLifeGame(80, 60, 12)
    game.run()

