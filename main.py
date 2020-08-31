import pygame
import sys
import pygame.freetype
import math

size = (1000, 800)  # 游戏窗体大小
if_game_start = False  # 游戏是否开始
num_chess = 0  # 对局双方累计下棋数
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

pos_board = [40, 40, 720, 720]  # 棋盘位置
pos_startGame_button = [400, 400, 200, 75]  # “开始游戏” 按钮框体位置
pos_endGame_button = [400, 550, 200, 75]  # “结束游戏” 按钮框体位置

pos_text_title = (200, 120)  # “围棋” 文字位置
pos_text_startGame = (410, 410)  # “开始游戏” 文字位置
pos_text_endGame = (410, 560)  # “结束游戏” 文字位置


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


# 开始对局并初始化对局几面
def start_game(screen):
    global if_game_start
    if_game_start = True
    chessBoard = pygame.image.load('GameData/img/board.png')
    screen.blit(chessBoard, [0, 0, 800, 802])


# 绘制棋子
def chess(screen, pos):
    global num_chess
    if num_chess % 2 == 0:
        pygame.draw.circle(screen, black, pos, 15)
    else:
        pygame.draw.circle(screen, white, pos, 15)
    num_chess += 1


# 处理鼠标点击事件
def deal_mouse_event(screen, event):
    if event.button == 1:  # 左键点击
        if not if_game_start:  # 未开始对局
            if is_in_area(event.pos, pos_endGame_button):  # 点击“结束游戏”按钮
                sys.exit()
            elif is_in_area(event.pos, pos_startGame_button):  # 点击“开始游戏”按钮
                start_game(screen)
        else:  # 开始对局
            if is_in_area(event.pos, pos_board):  # 合法落子
                piece = fix_pieces_pos(event.pos)
                chess(screen, piece)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)  # 设置窗口大小（宽度，高度）
    screen_rect = screen.get_rect()  # 初始化主图层全区域
    pygame.display.set_caption("围棋")  # 设置标题
    # 初始化背景
    bg = pygame.image.load('GameData/img/background.png')
    screen.blit(bg, screen_rect)
    # 绘制标题界面
    pygame.draw.rect(screen, red, pos_startGame_button, 5)  # 绘制按钮框体
    pygame.draw.rect(screen, red, pos_endGame_button, 5)

    font_title = pygame.font.Font('GameData/Font/HGDGY_CNKI.TTF', 180)  # 设置字体的类型和大小
    font_button = pygame.font.Font('GameData/Font/STXINGKA.TTF', 45)

    text_title = font_title.render("围    棋", True, black)
    text_startGame = font_button.render("开始游戏", True, red)  # 绘制文字，和blit()搭配使用
    text_endGame = font_button.render("退出游戏", True, red)

    screen.blit(text_title, pos_text_title)  # 绘制“围棋”
    screen.blit(text_startGame, pos_text_startGame)  # 绘制“开始游戏”
    screen.blit(text_endGame, pos_text_endGame)  # 绘制“结束游戏”
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
