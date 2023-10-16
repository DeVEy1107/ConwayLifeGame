import pygame
import sys

# 初始化Pygame
pygame.init()

# 创建窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("鼠标轨迹示例")


mouse_position = (0, 0)
mouse_positions = []
recording = False  

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 鼠标左键按下，开始记录轨迹
            recording = True
            mouse_positions = []  # 清空之前的轨迹
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # 鼠标左键释放，停止记录轨迹
            recording = False
        elif event.type == pygame.MOUSEMOTION and recording:
            # 记录鼠标轨迹
            mouse_position = event.pos
            mouse_positions.append(mouse_position)

    # 清空屏幕
    screen.fill((255, 255, 255))

    # 绘制鼠标轨迹
    if len(mouse_positions) > 1:
        pygame.draw.lines(screen, (0, 0, 0), False, mouse_positions, 2)

    pygame.display.flip()

# 退出Pygame
pygame.quit()
sys.exit()
