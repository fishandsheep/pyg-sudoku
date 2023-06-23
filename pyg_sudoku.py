import pygame
from pygame.locals import *
from sudoku import Sudoku

# 初始化
pygame.init()
# 设置窗口大小
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Sudoku")
# 字体设置
font = pygame.font.Font(None, 50)

numbers = '123456789'
# 输入框设置
input_boxs = []
rect = pygame.Rect(70, 70, 70, 70)
for i in range(9):
    for j in range(9):
        copy = rect.copy()
        copy.top += ((70 * i) + (i // 3) * 5)
        copy.left += ((70 * j) + (j // 3) * 5)
        input_boxs.append(copy)
# 记录输入的数字坐标和 [值,是否是初始化值,是否要增强显示]
dirt_value = {x: '' for x in range(81)}
dirt_init = {x: False for x in range(81)}
dirt_power = {x: False for x in range(81)}

# 初始化数独数字
puzzle = Sudoku(3).difficulty(0.5)
index = 0
for out_ls in puzzle.board:
    for item in out_ls:
        if item is not None:
            dirt_value[index] = str(item)
            dirt_init[index] = True
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


def check_input(current_index, in_list):
    for in_index in in_list:
        if current_index == in_index:
            continue
        if not dirt_power[in_index] and dirt_value[current_index] == dirt_value[in_index]:
            dirt_power[current_index] = True
            dirt_power[in_index] = True


while running:
    mouse_pos = pygame.mouse.get_pos()
    # 获取输入的数字
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.unicode in numbers:
                change_index = -1
                for i, input_box in enumerate(input_boxs):
                    # 鼠标悬停在非初始化值的按钮上
                    if input_box.collidepoint(mouse_pos) and not dirt_init[i]:
                        dirt_value[i] = event.unicode
                        change_index = i
                        break
                if change_index != -1:
                    # 初始化所有单元格
                    dirt_power = {x: False for x in range(81)}
                    # 循环全部的单元格
                    for key, value in dirt_value.items():
                        if dirt_value[key]:
                            check_input(key, w_group[key // 9])
                            check_input(key, h_group[key % 9])
                            for in_n_list in n_group:
                                if key in in_n_list:
                                    check_input(key, in_n_list)

    # 渲染输入框
    screen.fill((255, 255, 255))
    for i, key in enumerate(input_boxs):
        collide_point = key.collidepoint(mouse_pos)
        # 配色方案
        input_border_color = (0, 153, 0) if collide_point else (96, 96, 96)
        text_color = (204, 0, 0) if dirt_power[i] else (105, 105, 105)
        input_bg = (192, 192, 192) if dirt_init[i] else (255, 255, 255)
        # 绘制输入框背景
        pygame.draw.rect(screen, input_bg, key)
        # 绘制输入框边框
        pygame.draw.rect(screen, input_border_color, key, 1, 3)

        text_surface = font.render(dirt_value[i], True, text_color)
        text_rect = text_surface.get_rect(center=key.center)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

# 退出游戏
pygame.quit()
