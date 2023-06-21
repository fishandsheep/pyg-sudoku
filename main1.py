import pygame
from pygame.locals import *
from sudoku import Sudoku

# 初始化
pygame.init()

numbers = '123456789'

# 设置窗口大小
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Number Input")

# 字体设置
font = pygame.font.Font(None, 50)

# 输入框设置
input_boxs = []
rect = pygame.Rect(70, 70, 70, 70)
for i in range(9):
    for j in range(9):
        copy = rect.copy()
        copy.top += ((70 * i) + (i // 3) * 3)
        copy.left += ((70 * j) + (j // 3) * 3)
        input_boxs.append(copy)
# 记录输入的数字坐标和 [值,是否是初始化值,是否要增强显示]
dirt = {x: ['', False, False] for x in range(81)}

# 初始化数独数字
puzzle = Sudoku(3).difficulty(0.5)
index = 0
for out_ls in puzzle.board:
    for item in out_ls:
        if item is not None:
            dirt[index][0] = str(item)
            dirt[index][1] = True
        index += 1

# 初始化三个校验组，横向、纵向、九宫格
w_group = []
for i in range(9):
    in_group = [x for x in range(9 * i, 9 * (i + 1))]
    w_group.append(in_group)

h_group = []
for i in range(9):
    in_group = [x for x in range(i, 9 * 9, 9)]
    h_group.append(in_group)

n_group = []
for i in range(9):
    row_indices = []
    for j in range(9):
        index = i // 3 * 27 + i % 3 * 3 + j // 3 * 9 + j % 3
        row_indices.append(index)
    n_group.append(row_indices)

# 游戏循环
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    # 获取输入的数字
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.unicode in numbers:
                for i, input_box in enumerate(input_boxs):
                    # 鼠标悬停在非初始化值的按钮上
                    if input_box.collidepoint(mouse_pos) and not dirt[i][1]:
                        dirt[i][0] = event.unicode
                        # 初始化是否增强
                        dirt = {k: [v[0], v[1], False] for k, v in dirt.items()}
                        for w_ls in w_group:
                            subset_dict = {index: value for index, value in dirt.items() if index in w_ls}
                            duplicate_coordinates = [index for index, value in subset_dict.items() if
                                                     any(v == value[0] and v != '' for v in value)]
                            print(duplicate_coordinates)
    # 渲染输入框
    screen.fill((255, 255, 255))
    for i, key in enumerate(input_boxs):
        collide_point = key.collidepoint(mouse_pos)
        input_border_color = 'black' if collide_point else 'gray'
        # 绘制输入框和文本
        pygame.draw.rect(screen, input_border_color, key, 1)
        text_color = 'gray' if dirt[i][1] else ('red' if dirt[i][2] else 'green')
        text_surface = font.render(dirt[i][0], True, text_color)
        text_rect = text_surface.get_rect(center=key.center)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

# 退出游戏
pygame.quit()
