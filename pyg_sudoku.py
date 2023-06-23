import sys
import time
from random import randrange

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
rect = pygame.Rect(70, 20, 70, 70)
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


def check_input(current_index, in_list):
    for in_index in in_list:
        if current_index == in_index:
            continue
        if not dirt_power[in_index] and dirt_value[current_index] == dirt_value[in_index]:
            dirt_power[current_index] = True
            dirt_power[in_index] = True


# 定义计时器属性
rect_clock = pygame.Rect(250, 700, 80, 35)
timer_font = pygame.font.SysFont("Arial", 20)
timer_color = (105, 105, 105)  # 计时器文本颜色
timer_position = (400, 700)  # 计时器位置
# 定义计时变量
time_elapsed = 0
is_complete = False
clock = pygame.time.Clock()

dif_box = pygame.Rect(350, 700, 80, 35)
dif_font = pygame.font.SysFont("Arial", 20)
dif_value = 0.50

start_box = pygame.Rect(450, 700, 80, 35)
start_font = pygame.font.SysFont("Arial", 20)

# 游戏循环
running = True
while running:
    is_start = False
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 检测鼠标左键单击
                start_hover = start_box.collidepoint(mouse_pos)
                if start_hover:
                    pygame.draw.rect(screen, (0, 153, 0), start_box)
                    pygame.draw.rect(screen, (105, 105, 105), start_box, 1, 3)
                    start_text = start_font.render('start', True, (105, 105, 105))
                    start_text_rect = start_text.get_rect(center=start_box.center)
                    screen.blit(start_text, start_text_rect)
                    time_elapsed = 0
                    is_complete = False
                    is_start = True
                    time.sleep(0.4)
                    pygame.display.flip()
            dif_hover = dif_box.collidepoint(mouse_pos)
            if dif_hover:
                pygame.draw.rect(screen, (105, 105, 105), dif_box, 1, 3)
                dif_text = dif_font.render(f'{dif_value:.2f}', True, (105, 105, 105))
                dif_text_rect = dif_text.get_rect(center=dif_box.center)
                screen.blit(dif_text, dif_text_rect)
                if event.button == 4:  # 检测鼠标滚轮向上滚动
                    dif_value += 0.01
                elif event.button == 5:  # 检测鼠标滚轮向下滚动
                    dif_value -= 0.01
                pygame.display.flip()
    # 初始化数独数字
    if dif_value >= 1:
        dif_value = 0.99
    elif dif_value <= 0:
        dif_value = 0.01
    if is_start:
        puzzle = Sudoku(3, 3, seed=randrange(sys.maxsize)).difficulty(dif_value)
        # 记录输入的数字坐标和 [值,是否是初始化值,是否要增强显示]
        dirt_value = {x: '' for x in range(81)}
        dirt_init = {x: False for x in range(81)}
        dirt_power = {x: False for x in range(81)}
        index = 0
        for out_ls in puzzle.board:
            for item in out_ls:
                if item:
                    dirt_value[index] = str(item)
                    dirt_init[index] = True
                index += 1

    # 渲染输入框
    screen.fill((255, 255, 255))
    for i, key in enumerate(input_boxs):
        collide_point = key.collidepoint(mouse_pos)
        # 配色方案
        input_border_color = (0, 153, 0) if collide_point and not dirt_init[i] else (96, 96, 96)
        text_color = (204, 0, 0) if dirt_power[i] else (105, 105, 105)
        input_bg = (192, 192, 192) if dirt_init[i] else (255, 255, 255)
        # 绘制输入框背景
        pygame.draw.rect(screen, input_bg, key)
        # 绘制输入框边框
        pygame.draw.rect(screen, input_border_color, key, 1, 3)

        text_surface = font.render(dirt_value[i], True, text_color)
        text_rect = text_surface.get_rect(center=key.center)
        screen.blit(text_surface, text_rect)

    # 判断是否完成
    if not is_complete:
        sum_value = 0
        for value in dirt_value.values():
            sum_value += int(value) if value else 0
        is_complete = sum_value == 45 * 9
        # 更新计时器
        time_elapsed += clock.tick(60)  # 以毫秒为单位更新计时器（60帧每秒）

    # 绘制计时器文本
    elapsed_second = time_elapsed // 1000
    minute = str(elapsed_second // 60).zfill(2)
    second = str(elapsed_second % 60).zfill(2)
    pygame.draw.rect(screen, (0, 153, 0) if is_complete else (105, 105, 105), rect_clock, 1, 3)
    timer_text = timer_font.render(f'{minute}:{second}', True, (0, 153, 0) if is_complete else (105, 105, 105))
    timer_text_rect = timer_text.get_rect(center=rect_clock.center)
    screen.blit(timer_text, timer_text_rect)

    # 难度框
    dif_hover = dif_box.collidepoint(mouse_pos)
    # 绘制输入框背景
    pygame.draw.rect(screen, (192, 192, 192) if dif_hover else (255, 255, 255), dif_box)
    pygame.draw.rect(screen, (105, 105, 105), dif_box, 1, 3)
    dif_text = dif_font.render(f'{dif_value:.2f}', True, (105, 105, 105))
    dif_text_rect = dif_text.get_rect(center=dif_box.center)
    screen.blit(dif_text, dif_text_rect)

    # 开始框
    start_hover = start_box.collidepoint(mouse_pos)
    # 绘制输入框背景
    pygame.draw.rect(screen, (192, 192, 192) if start_hover else (255, 255, 255), start_box)
    pygame.draw.rect(screen, (105, 105, 105), start_box, 1, 3)
    start_text = start_font.render('start', True, (105, 105, 105))
    start_text_rect = start_text.get_rect(center=start_box.center)
    screen.blit(start_text, start_text_rect)

    pygame.display.flip()
# 退出游戏
pygame.quit()
