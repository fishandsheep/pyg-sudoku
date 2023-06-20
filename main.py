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
font = pygame.font.Font(None, 30)

# 输入框设置
input_boxs = [pygame.Rect(10, 10, 30, 30), pygame.Rect(40, 10, 30, 30), pygame.Rect(70, 10, 30, 30),
              pygame.Rect(100, 10, 30, 30), pygame.Rect(130, 10, 30, 30), pygame.Rect(160, 10, 30, 30),
              pygame.Rect(190, 10, 30, 30), pygame.Rect(220, 10, 30, 30), pygame.Rect(250, 10, 30, 30),

              pygame.Rect(10, 40, 30, 30), pygame.Rect(40, 40, 30, 30), pygame.Rect(70, 40, 30, 30),
              pygame.Rect(10, 70, 30, 30), pygame.Rect(40, 70, 30, 30), pygame.Rect(70, 70, 30, 30)]

input_boxs = [pygame.Rect(10, 10, 30, 30), pygame.Rect(40, 10, 30, 30), pygame.Rect(70, 10, 30, 30),
              pygame.Rect(10, 40, 30, 30), pygame.Rect(40, 40, 30, 30), pygame.Rect(70, 40, 30, 30),
              pygame.Rect(10, 70, 30, 30), pygame.Rect(40, 70, 30, 30), pygame.Rect(70, 70, 30, 30)]

dirt = {1: {'value': '', 'font_color': ''},
        2: {'value': '', 'font_color': ''},
        3: {'value': '', 'font_color': ''},
        4: {'value': '', 'font_color': ''},
        5: {'value': '', 'font_color': ''},
        6: {'value': '', 'font_color': ''},
        7: {'value': '', 'font_color': ''},
        8: {'value': '', 'font_color': ''},
        9: {'value': '', 'font_color': ''}}
# 值出现的次数
dirt_values = {}
# 游戏循环
running = True
while running:
    # 获取输入的数字
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.unicode in numbers:
                for i, input_box in enumerate(input_boxs):
                    # 检测鼠标是否悬停在按钮上
                    if input_box.collidepoint(mouse_pos):
                        dirt[i + 1]['value'] = event.unicode
                        if event.unicode in dirt_values.keys():
                            dirt_values[event.unicode] = dirt_values[event.unicode] + 1
                        else:
                            dirt_values[event.unicode] = 1
                        break

    for k, v in dirt.items():
        if v['value'] == '':
            v['font_color'] = 'green'
        else:
            if dirt_values[v['value']] > 1:
                v['font_color'] = 'red'
            else:
                v['font_color'] = 'green'

    screen.fill((255, 255, 255))
    for i, key in enumerate(input_boxs):
        # 绘制输入框和文本
        color = 'black' if key.collidepoint(mouse_pos) else 'gray'
        pygame.draw.rect(screen, color, key, 1)
        text_surface = font.render(dirt[i + 1]['value'], True, dirt[i + 1]['font_color'])
        text_rect = text_surface.get_rect(center=key.center)
        screen.blit(text_surface, text_rect)
    pygame.display.flip()

# 退出游戏
pygame.quit()
