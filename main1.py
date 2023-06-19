import pygame
from pygame.locals import *

# 初始化
pygame.init()

numbers = '123456789'

# 设置窗口大小
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Number Input")

# 字体设置
font = pygame.font.Font(None, 60)

# 输入框设置
input_boxs = []
rect = pygame.Rect(70, 70, 70, 70)
for i in range(9):
    for j in range(9):
        copy = rect.copy()
        copy.bottom
        copy.left += ((70 * i) + (i // 3) * 3)
        copy.top += ((70 * j) + (j // 3) * 3)
        input_boxs.append(copy)

# 游戏循环
running = True
while running:
    # 获取输入的数字
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill((255, 255, 255))
    for i, key in enumerate(input_boxs):
        # 绘制输入框和文本
        color = 'black' if key.collidepoint(mouse_pos) else 'gray'
        pygame.draw.rect(screen, color, key, 1)
        text_surface = font.render('', True, 'green')
        text_rect = text_surface.get_rect(center=key.center)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

# 退出游戏
pygame.quit()
