import sys
from random import randrange

import pygame
from pygame.locals import QUIT, KEYDOWN
from sudoku import Sudoku

pygame.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Sudoku")

numbers = '123456789'
# main input box
font = pygame.font.Font(None, 50)
input_boxes = []
rect = pygame.Rect(70, 20, 70, 70)
for i in range(9):
    for j in range(9):
        copy = rect.copy()
        copy.top += ((70 * i) + (i // 3) * 5)
        copy.left += ((70 * j) + (j // 3) * 5)
        input_boxes.append(copy)

# box value,box has init value, box focus
box_value, box_init, box_focus = {x: '' for x in range(81)}, \
    {x: False for x in range(81)}, \
    {x: False for x in range(81)}
# three group : horizontal, vertical, nine-box grid
h_group, v_group, n_group = [], [], []
for i in range(9):
    in_group = [x for x in range(9 * i, 9 * (i + 1))]
    h_group.append(in_group)
    in_group = [x for x in range(i, 9 * 9, 9)]
    v_group.append(in_group)
    row_indices = []
    for j in range(9):
        index = i // 3 * 27 + i % 3 * 3 + j // 3 * 9 + j % 3
        row_indices.append(index)
    n_group.append(row_indices)

# complete all calibrations
is_complete = False


# check input value
def check_input(current_index, in_list):
    for in_index in in_list:
        if current_index == in_index:
            continue
        if not box_focus[in_index] and box_value[current_index] == box_value[in_index]:
            box_focus[current_index] = True
            box_focus[in_index] = True


# bottom
mini_font = pygame.font.SysFont("Arial", 20)
time_clock_box, dif_box, start_box = pygame.Rect(250, 700, 80, 35), \
    pygame.Rect(350, 700, 80, 35), \
    pygame.Rect(450, 700, 80, 35)
clock = pygame.time.Clock()
# init time clock
time_elapsed = 0
# init difficulty
dif_value = 0.50

# define some color
white = (255, 255, 255)
green = (0, 153, 0)
light_gray = (192, 192, 192)
deep_gray = (105, 105, 105)
red = (204, 0, 0)

running = True
while running:
    is_start = False
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.unicode in numbers:
                change_index = -1
                for i, input_boxes in enumerate(input_boxes):
                    if input_boxes.collidepoint(mouse_pos) and not box_init[i]:
                        box_value[i] = event.unicode
                        change_index = i
                        break
                if change_index != -1:
                    box_focus = {x: False for x in range(81)}
                    # check all cells
                    for key, value in box_value.items():
                        if box_value[key]:
                            check_input(key, h_group[key // 9])
                            check_input(key, v_group[key % 9])
                            for in_n_list in n_group:
                                if key in in_n_list:
                                    check_input(key, in_n_list)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button click
                start_hover = start_box.collidepoint(mouse_pos)
                if start_hover:
                    pygame.draw.rect(screen, green, start_box)
                    pygame.draw.rect(screen, deep_gray, start_box, 1, 3)
                    start_text = mini_font.render('start', True, deep_gray)
                    start_text_rect = start_text.get_rect(center=start_box.center)
                    screen.blit(start_text, start_text_rect)
                    time_elapsed = 0
                    is_complete = False
                    is_start = True
                    pygame.display.flip()
            dif_hover = dif_box.collidepoint(mouse_pos)
            if dif_hover:
                pygame.draw.rect(screen, deep_gray, dif_box, 1, 3)
                dif_text = mini_font.render(f'{dif_value:.2f}', True, deep_gray)
                dif_text_rect = dif_text.get_rect(center=dif_box.center)
                screen.blit(dif_text, dif_text_rect)
                if event.button == 4:  # mouse wheel up
                    dif_value += 0.01
                elif event.button == 5:  # mouse wheel down
                    dif_value -= 0.01
                pygame.display.flip()

    # difficulty limit
    if dif_value >= 1:
        dif_value = 0.99
    elif dif_value <= 0:
        dif_value = 0.01
    if is_start:
        puzzle = Sudoku(3, 3, seed=randrange(sys.maxsize)).difficulty(dif_value)
        box_value, box_init, box_focus = {x: '' for x in range(81)}, \
            {x: False for x in range(81)}, \
            {x: False for x in range(81)}
        index = 0
        for out_ls in puzzle.board:
            for item in out_ls:
                if item:
                    box_value[index] = str(item)
                    box_init[index] = True
                index += 1

    screen.fill(white)

    # draw all cells
    for i, key in enumerate(input_boxes):
        pygame.draw.rect(screen, light_gray if box_init[i] else white, key)
        pygame.draw.rect(screen, green if key.collidepoint(mouse_pos) and not box_init[i] else deep_gray, key,
                         2 if key.collidepoint(mouse_pos) and not box_init[i] else 1, 3)
        text_surface = font.render(box_value[i], True, red if box_focus[i] else deep_gray)
        text_rect = text_surface.get_rect(center=key.center)
        screen.blit(text_surface, text_rect)

    if not is_complete:
        sum_value = 0
        for value in box_value.values():
            sum_value += int(value) if value else 0
        is_complete = sum_value == 45 * 9
        # update time elapsed 60fps = 1s
        time_elapsed += clock.tick(60)

    # draw timer clock
    elapsed_second = time_elapsed // 1000
    minute = str(elapsed_second // 60).zfill(2)
    second = str(elapsed_second % 60).zfill(2)
    pygame.draw.rect(screen, green if is_complete else deep_gray, time_clock_box, 1, 3)
    timer_text = mini_font.render(f'{minute}:{second}', True, green if is_complete else deep_gray)
    timer_text_rect = timer_text.get_rect(center=time_clock_box.center)
    screen.blit(timer_text, timer_text_rect)

    # draw difficulty box
    pygame.draw.rect(screen, light_gray if dif_box.collidepoint(mouse_pos) else white, dif_box)
    pygame.draw.rect(screen, deep_gray, dif_box, 1, 3)
    dif_text = mini_font.render(f'{dif_value:.2f}', True, deep_gray)
    dif_text_rect = dif_text.get_rect(center=dif_box.center)
    screen.blit(dif_text, dif_text_rect)

    # draw start box
    pygame.draw.rect(screen, light_gray if start_box.collidepoint(mouse_pos) else white, start_box)
    pygame.draw.rect(screen, deep_gray, start_box, 1, 3)
    start_text = mini_font.render('start', True, deep_gray)
    start_text_rect = start_text.get_rect(center=start_box.center)
    screen.blit(start_text, start_text_rect)

    pygame.display.flip()
pygame.quit()
