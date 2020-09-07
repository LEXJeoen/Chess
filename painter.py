import pygame
import pygame.freetype

from Players import Player
from goBoard import Board
from utils import Point

size = (1000, 800)  # 游戏窗体大小
piece_radius = 15

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
color_button_main_menu = (255, 0, 0)
color_button_selectGameMode_menu = (255, 69, 0)

pos_board = [40, 40, 720, 720]  # 棋盘位置
pos_startGame_button = [400, 400, 200, 75]  # “开始游戏” 按钮框体位置
pos_endGame_button = [400, 550, 200, 75]  # “结束游戏” 按钮框体位置
pos_doubleHuman_button = [400, 400, 200, 75]  # “双人对局” 按钮框体位置
pos_HumanAndAI_button = [400, 500, 200, 75]  # “人机对局” 按钮框体位置
pos_AIAndAI_button = [400, 600, 200, 75]  # “机机对局” 按钮框体位置
pos_restart_button = [805, 170, 165, 60]  # “重新开始” 按钮框体位置
pos_regret_button = [805, 270, 165, 60]  # “悔棋” 按钮框体位置
pos_pass_button = [805, 370, 165, 60]  # “过棋” 按钮框体位置
pos_resign_button = [805, 470, 165, 60]  # “认输” 按钮框体位置
pos_turn_back_button = [850, 570, 70, 70]  # 返回按钮位置

pos_text_title = (200, 120)  # “围棋” 文字位置
pos_text_startGame = (410, 410)  # “开始游戏” 文字位置
pos_text_endGame = (410, 560)  # “结束游戏” 文字位置
pos_text_doubleHuman = (410, 410)  # “双人对局” 文字位置
pos_text_HumanAndAI = (410, 510)  # “人机对局” 文字位置
pos_text_AIAndAI = (410, 610)  # “机机对局” 文字位置
pos_text_restart = (805, 180)  # “重新开始” 文字位置
pos_text_regret = (830, 280)  # “悔棋” 文字位置
pos_text_pass = (830, 380)  # “过棋” 文字位置
pos_text_resign = (830, 480)  # “认输” 文字位置

pos_white_win = [300, 300, 500, 500]  # 白方胜利图片
pos_black_win = [0, 300, 500, 500]  # 黑方胜利图片

bg = pygame.image.load('GameData/img/background.png')  # 背景图片
chessBoard = pygame.image.load('GameData/img/board.png')  # 棋盘
turn_back = pygame.image.load('GameData/img/返回按钮.png')
white_win = pygame.image.load('GameData/img/白棋胜利.png')
black_win = pygame.image.load('GameData/img/黑棋胜利.png')


# 绘制棋盘
def draw_chessBoard(screen):
    screen.blit(chessBoard, (0, 0))


# 绘制对局界面的按钮
def draw_startGame_menu(screen, game_mode):
    pygame.draw.rect(screen, color_button_main_menu, pos_restart_button, 5)  # 绘制按钮框体

    font_button = pygame.font.Font('GameData/Font/STXINGKA.TTF', 40)

    text_gameMode = font_button.render("重新开始", True, color_button_main_menu)  # 绘制文字，和blit()搭配使用
    screen.blit(text_gameMode, pos_text_restart)  # 绘制“重新开始”

    screen.blit(turn_back,pos_turn_back_button)

    if game_mode == 1 or game_mode == 2:
        pygame.draw.rect(screen, color_button_main_menu, pos_regret_button, 5)
        pygame.draw.rect(screen, color_button_main_menu, pos_pass_button, 5)
        pygame.draw.rect(screen, color_button_main_menu, pos_resign_button, 5)

        text_regret = font_button.render("悔  棋", True, color_button_main_menu)
        text_pass = font_button.render("过  棋", True, color_button_main_menu)
        text_surrender = font_button.render("认  输", True, color_button_main_menu)

        screen.blit(text_regret, pos_text_regret)  # 绘制“悔棋”
        screen.blit(text_pass, pos_text_pass)  # 绘制“过棋”
        screen.blit(text_surrender, pos_text_resign)  # 绘制“认输”


# 绘制主界面菜单
def draw_main_menu(screen):
    # 绘制标题界面
    pygame.draw.rect(screen, color_button_main_menu, pos_startGame_button, 5)  # 绘制按钮框体
    pygame.draw.rect(screen, color_button_main_menu, pos_endGame_button, 5)

    font_button = pygame.font.Font('GameData/Font/STXINGKA.TTF', 45)

    text_startGame = font_button.render("开始游戏", True, color_button_main_menu)  # 绘制文字，和blit()搭配使用
    text_endGame = font_button.render("退出游戏", True, color_button_main_menu)

    screen.blit(text_startGame, pos_text_startGame)  # 绘制“开始游戏”
    screen.blit(text_endGame, pos_text_endGame)  # 绘制“结束游戏”


# 绘制选择游戏模式菜单
def draw_sclectGameMode_menu(screen):
    pygame.draw.rect(screen, color_button_selectGameMode_menu, pos_doubleHuman_button, 5)  # 绘制按钮框体
    pygame.draw.rect(screen, color_button_selectGameMode_menu, pos_HumanAndAI_button, 5)  # 绘制按钮框体
    pygame.draw.rect(screen, color_button_selectGameMode_menu, pos_AIAndAI_button, 5)  # 绘制按钮框体

    font_button = pygame.font.Font('GameData/Font/STXINGKA.TTF', 45)

    text_doubleHuman = font_button.render("双人对局", True, color_button_selectGameMode_menu)  # 绘制文字，和blit()搭配使用
    text_HumanAndAI = font_button.render("人机对局", True, color_button_selectGameMode_menu)  # 绘制文字，和blit()搭配使用
    text_AIAndAI = font_button.render("机机对局", True, color_button_selectGameMode_menu)  # 绘制文字，和blit()搭配使用

    screen.blit(text_doubleHuman, pos_text_doubleHuman)
    screen.blit(text_HumanAndAI, pos_text_HumanAndAI)
    screen.blit(text_AIAndAI, pos_text_AIAndAI)


# 擦除对象
def clear_source(screen, source, sourceType):
    if sourceType == 'buttons':
        length = len(source)
        clear_left = source[0][0] - 5
        clear_top = source[0][1] - 5
        clear_width = source[0][2] + 10
        clear_height = source[length - 1][1] + source[length - 1][3] + 10
        clear_rect = pygame.Rect(clear_left, clear_top, clear_width, clear_height)
        screen.blit(bg, clear_rect, clear_rect)  # 擦除现有按钮
    elif sourceType == 'stone':
        clear_left = source[0] - (piece_radius + 5)
        clear_top = source[1] - (piece_radius + 5)
        clear_width = 40
        clear_height = 40
        clear_rect = pygame.Rect(clear_left, clear_top, clear_width, clear_height)
        screen.blit(chessBoard, clear_rect, clear_rect)  # 擦除单个棋子


# 绘制主界面
def draw_main_interface(screen):
    screen_rect = screen.get_rect()  # 获取主图层全区域
    # 初始化背景
    screen.blit(bg, screen_rect)

    font_title = pygame.font.Font('GameData/Font/HGDGY_CNKI.TTF', 180)  # 设置字体的类型和大小
    text_title = font_title.render("围    棋", True, black)
    screen.blit(text_title, pos_text_title)  # 绘制“围棋”

    draw_main_menu(screen)


# 绘制棋子
def draw_new_stone(screen, point, player):
    pos = (point.row * 40, point.col * 40)
    if player == Player.black:
        pygame.draw.circle(screen, black, pos, piece_radius)
    else:
        pygame.draw.circle(screen, white, pos, piece_radius)


def draw_stones(board, screen):
    # print("start draw")
    for r in range(1, board.num_rows + 1):
        for c in range(1, board.num_cols + 1):
            point = Point(row=r, col=c)
            if board.get(point) == Player.black:
                # print("black", r, c)
                pos = (point.row * 40, point.col * 40)
                pygame.draw.circle(screen, black, pos, piece_radius)
            elif board.get(point) == Player.white:
                # print("white", r, c)
                pos = (point.row * 40, point.col * 40)
                pygame.draw.circle(screen, white, pos, piece_radius)
    # print(" ")


# 显示胜利方
def show_winner(winner, screen):
    if winner == Player.black:
        screen.blit(black_win, pos_black_win)
    elif winner == Player.white:
        screen.blit(white_win, pos_white_win)
