import pygame
import sys
import pygame.freetype
import math

size = (1000, 800)  # 游戏窗体大小
if_game_start = False  # 是否点击开始
if_game_end = False  # 对局是否结束
num_chess = 0  # 对局双方累计下棋数
game_mode = 0  # 0是未选择模式；1是双人对战；2是人机对战；3是机机对战
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
pos_surrender_button = [805, 470, 165, 60]  # “认输” 按钮框体位置

pos_text_title = (200, 120)  # “围棋” 文字位置
pos_text_startGame = (410, 410)  # “开始游戏” 文字位置
pos_text_endGame = (410, 560)  # “结束游戏” 文字位置
pos_text_doubleHuman = (410, 410)  # “双人对局” 文字位置
pos_text_HumanAndAI = (410, 510)  # “人机对局” 文字位置
pos_text_AIAndAI = (410, 610)  # “机机对局” 文字位置
pos_text_restart = (805, 180)  # “重新开始” 文字位置
pos_text_regret = (830, 280)  # “悔棋” 文字位置
pos_text_pass = (830, 380)  # “过棋” 文字位置
pos_text_surrender = (830, 480)  # “认输” 文字位置

pos_white_win = [300, 300, 500, 500]  # 白方胜利图片
pos_black_win = [0, 300, 500, 500]  # 黑方胜利图片

chess_history = []

bg = pygame.image.load('GameData/img/background.png')  # 背景图片
chessBoard = pygame.image.load('GameData/img/board.png')  # 棋盘
white_win = pygame.image.load('GameData/img/白棋胜利.png')
black_win = pygame.image.load('GameData/img/黑棋胜利.png')


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


# 绘制棋盘
def draw_chessBoard(screen):
    global chessBoard
    screen.blit(chessBoard, (0, 0))


# 绘制对局界面的按钮
def draw_startGame_menu(screen):
    pygame.draw.rect(screen, color_button_main_menu, pos_restart_button, 5)  # 绘制按钮框体

    font_button = pygame.font.Font('GameData/Font/STXINGKA.TTF', 40)

    text_gameMode = font_button.render("重新开始", True, color_button_main_menu)  # 绘制文字，和blit()搭配使用
    screen.blit(text_gameMode, pos_text_restart)  # 绘制“重新开始”

    global game_mode
    if game_mode == 1 or game_mode == 2:
        pygame.draw.rect(screen, color_button_main_menu, pos_regret_button, 5)
        pygame.draw.rect(screen, color_button_main_menu, pos_pass_button, 5)
        pygame.draw.rect(screen, color_button_main_menu, pos_surrender_button, 5)

        text_regret = font_button.render("悔  棋", True, color_button_main_menu)
        text_pass = font_button.render("过  棋", True, color_button_main_menu)
        text_surrender = font_button.render("认  输", True, color_button_main_menu)

        screen.blit(text_regret, pos_text_regret)  # 绘制“悔棋”
        screen.blit(text_pass, pos_text_pass)  # 绘制“过棋”
        screen.blit(text_surrender, pos_text_surrender)  # 绘制“认输”


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
    elif sourceType == 'piece':
        clear_left = source[0] - (piece_radius + 5)
        clear_top = source[1] - (piece_radius + 5)
        clear_width = 40
        clear_height = 40
        clear_rect = pygame.Rect(clear_left, clear_top, clear_width, clear_height)
        screen.blit(chessBoard, clear_rect, clear_rect)  # 擦除棋子


# 绘制主界面
def draw_main_interface(screen):
    screen_rect = screen.get_rect()  # 获取主图层全区域
    # 初始化背景
    global bg
    screen.blit(bg, screen_rect)

    font_title = pygame.font.Font('GameData/Font/HGDGY_CNKI.TTF', 180)  # 设置字体的类型和大小
    text_title = font_title.render("围    棋", True, black)
    screen.blit(text_title, pos_text_title)  # 绘制“围棋”

    draw_main_menu(screen)


# 绘制棋子
def chess(screen, pos):
    global num_chess
    if num_chess % 2 == 0:
        pygame.draw.circle(screen, black, pos, piece_radius)
        chess_history.append(pos)
    else:
        pygame.draw.circle(screen, white, pos, piece_radius)
        chess_history.append(pos)
    num_chess += 1


def regret(screen):
    global num_chess
    if num_chess > 0:
        clear_source(screen, chess_history[-1], 'piece')
        num_chess -= 1
        del chess_history[-1]


# 显示胜利方
def show_winner(screen):
    global num_chess, if_game_end
    if num_chess % 2 == 0:
        screen.blit(white_win, pos_white_win)
    else:
        screen.blit(black_win, pos_black_win)
    if_game_end = True


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
                            piece = fix_pieces_pos(event.pos)
                            chess(screen, piece)
                        elif is_in_area(event.pos, pos_regret_button):  # 点击“悔棋”
                            regret(screen)
                        elif is_in_area(event.pos, pos_pass_button):  # 点击“过棋”
                            num_chess += 1
                        elif is_in_area(event.pos, pos_surrender_button):  # 点击“认输”
                            show_winner(screen)
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
                draw_startGame_menu(screen)


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
