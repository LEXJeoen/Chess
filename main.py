import pygame
import sys
import pygame.freetype
import math
from painter import *

if_game_start = False  # 是否点击开始
if_game_end = False  # 对局是否结束
num_chess = 0  # 对局双方累计下棋数
game_mode = 0  # 0是未选择模式；1是双人对战；2是人机对战；3是机机对战

chess_history = []


# 判断鼠标是否点击指定范围内
def is_in_area(pos_mouse, area):
    """
    :param pos_mouse: 鼠标点击坐标
    :param area: 指定区域
    :return: in True out False
    """
    x, y = pos_mouse
    left, top, width, height = area
    if left <= x <= left + width and top <= y <= top + height:
        return True
    else:
        return False


# 修正落子位置
def fix_pieces_pos(pos):
    """
    棋盘大小：（40*40）*18*18
    起始坐标（棋盘左上角相对窗体左上角）：（40,40）
    :param pos: 鼠标点击位置坐标（double type）
    :return: 修正后的正确落子坐标（int type）
    """
    quotient_x = math.floor(pos[0] / 40)
    quotient_y = math.floor(pos[1] / 40)
    remainder_x = pos[0] % 40
    remainder_y = pos[1] % 40

    if remainder_x >= 20:
        quotient_x += 1
    if remainder_y >= 20:
        quotient_y += 1

    x = int(quotient_x * 40)
    y = int(quotient_y * 40)

    new_pos = (x, y)
    return new_pos


# 悔棋
def regret(screen):
    global num_chess
    if num_chess > 0:
        clear_source(screen, chess_history[-1], 'stone')
        num_chess -= 1
        del chess_history[-1]


# 跳转到游戏模式选择菜单
def select_gameMode(screen):
    global if_game_start
    if_game_start = True

    clear_list = [pos_startGame_button, pos_endGame_button]
    clear_source(screen, clear_list, 'buttons')

    draw_sclectGameMode_menu(screen)


# 处理鼠标点击事件
def deal_mouse_event(screen, event):
    global game_mode, num_chess, if_game_end
    if event.button == 1:  # 左键点击
        if not if_game_start:  # 未点击开始
            if is_in_area(event.pos, pos_endGame_button):  # 点击“结束游戏”按钮
                sys.exit()
            elif is_in_area(event.pos, pos_startGame_button):  # 点击“开始游戏”按钮
                select_gameMode(screen)
        else:  # 点击开始
            if game_mode != 0:  # 选择了游戏模式
                if is_in_area(event.pos, pos_restart_button):  # 点击“重新开始”
                    draw_chessBoard(screen)
                    num_chess = 0
                    if_game_end = False
                if not if_game_end:  # 当前对局未结束时以下功能可用
                    if game_mode == 1 or game_mode == 2:  # “机机对局”只有“重新开始”选项
                        if is_in_area(event.pos, pos_board):  # 合法落子
                            stone = fix_pieces_pos(event.pos)
                            chess(screen, stone, num_chess)
                            chess_history.append(stone)
                            num_chess += 1
                        elif is_in_area(event.pos, pos_regret_button):  # 点击“悔棋”
                            regret(screen)
                        elif is_in_area(event.pos, pos_pass_button):  # 点击“过棋”
                            num_chess += 1
                        elif is_in_area(event.pos, pos_surrender_button):  # 点击“认输”
                            show_winner(screen, num_chess)
                            if_game_end = True
            else:  # 未选择游戏模式
                if is_in_area(event.pos, pos_doubleHuman_button):  # 点击“双人对局”按钮
                    game_mode = 1
                    print(game_mode)
                elif is_in_area(event.pos, pos_HumanAndAI_button):  # 点击“双人对局”按钮
                    game_mode = 2
                    print(game_mode)
                elif is_in_area(event.pos, pos_AIAndAI_button):  # 点击“双人对局”按钮
                    game_mode = 3
                    print(game_mode)
                draw_chessBoard(screen)
                draw_startGame_menu(screen, game_mode)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)  # 设置窗口大小（宽度，高度）
    pygame.display.set_caption("围棋")  # 设置标题

    draw_main_interface(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                deal_mouse_event(screen, event)
            '''
            elif event.type == pygame.MOUSEMOTION:
                print(event.pos)
            '''
        pygame.display.update()  # 刷新屏幕，显示更新


if __name__ == '__main__':
    main()
