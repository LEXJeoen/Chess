import pygame
import sys
import pygame.freetype
import math
import copy
import time

from painter import *
from Board import *
from Players import Player, Human, RandomBot
from utils import Point, Move
from scoring import compute_game_result

if_click_start = False  # 是否点击开始
# self.if_game_end = False  # 对局是否结束
# self.num_chess = 0  # 对局双方累计下棋数
game_mode = 0  # 0是未选择模式；1是双人对战；2是人机对战；3是机机对战

game = None


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


'''
# 悔棋
def regret(screen):
    global num_chess
    if num_chess > 0:
        clear_source(screen, chess_history[-1], 'stone')
        num_chess -= 1
        del chess_history[-1]
'''


# 跳转到游戏模式选择菜单
def select_gameMode(screen):
    global if_click_start
    if_click_start = True

    clear_list = [pos_startGame_button, pos_endGame_button]
    clear_source(screen, clear_list, 'buttons')

    draw_sclectGameMode_menu(screen)


def playGame(screen, event):
    global game
    if game_mode == 1:
        if is_in_area(event.pos, pos_restart_button):  # 点击“重新开始”
            move = Move(is_restart=True)
            game = game.apply_move(move)
            draw_chessBoard(screen)
        if not game.is_over():  # 当前对局未结束时以下功能可用
            if is_in_area(event.pos, pos_board):  # 合法落子
                point = Human.go_strategy(event.pos)
                move = Move.play(point)
                game = game.apply_move(move)

                draw_stones(game.board, screen)
            elif is_in_area(event.pos, pos_pass_button):  # 点击“过棋”
                move = Move(is_pass=True)
                game = game.apply_move(move)
            elif is_in_area(event.pos, pos_resign_button):  # 点击“认输”
                move = Move(is_resign=True)
                game = game.apply_move(move)
                print(game.is_over())
                show_winner(game.next_player, screen)
    elif game_mode == 2:
        bot = RandomBot()
        if is_in_area(event.pos, pos_restart_button):  # 点击“重新开始”
            move = Move(is_restart=True)
            game = game.apply_move(move)
            draw_chessBoard(screen)
        if not game.is_over():  # 当前对局未结束时以下功能可用
            if is_in_area(event.pos, pos_board):  # 合法落子
                if game.next_player == Player.black:
                    point = Human.go_strategy(event.pos)
                    move = Move.play(point)
                    game = game.apply_move(move)
                    if if_can_play_stone:
                        move = bot.select_move(game)
                        game = game.apply_move(move)
                draw_stones(game.board, screen)
            elif is_in_area(event.pos, pos_pass_button):  # 点击“过棋”
                move = Move(is_pass=True)
                game = game.apply_move(move)
                move = bot.select_move(game)
                game = game.apply_move(move)
                draw_stones(game.board, screen)
            elif is_in_area(event.pos, pos_resign_button):  # 点击“认输”
                move = Move(is_resign=True)
                game = game.apply_move(move)
                print(game.is_over())
                show_winner(game.next_player, screen)
    elif game_mode == 3:
        pass


# 处理鼠标点击事件
def Handle_event(screen, event,bots):
    global if_click_start, game_mode, game
    if event.button == 1:  # 左键点击
        if not if_click_start:  # 未点击开始
            if is_in_area(event.pos, pos_endGame_button):  # 点击“结束游戏”按钮
                sys.exit()
            elif is_in_area(event.pos, pos_startGame_button):  # 点击“开始游戏”按钮
                select_gameMode(screen)
        else:  # 点击开始
            if game_mode != 0:  # 选择了游戏模式
                playGame(screen, event)

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


class Game():
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        self.last_move = move

    @classmethod
    def new_game(cls):
        board = Board(19, 19)
        return Game(board, Player.black, None, None)

    def apply_move(self, move):  # <1>
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)

            return Game(next_board, self.next_player.other, self, move)
        elif move.is_resign or move.is_pass:
            next_board = self.board
            return Game(next_board, self.next_player.other, self, move)
        elif move.is_restart:
            return Game.new_game()

            # tag::self_capture[]

    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0
        # end::self_capture[]

        # tag::is_ko[]

    @property
    def situation(self):
        return self.next_player, self.board

    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board)
        past_state = self.previous_state
        while past_state is not None:
            if past_state.situation == next_situation:
                return True
            past_state = past_state.previous_state
        return False

    # end::is_ko[]

    # tag::is_valid_move[]
    def is_valid_move(self, move):
        if self.is_over():
            return False
        if move.is_pass or move.is_resign:
            return True
        return (
                self.board.get(move.point) is None and
                not self.is_move_self_capture(self.next_player, move) and
                not self.does_move_violate_ko(self.next_player, move))

    # end::is_valid_move[]

    # tag::is_over[]
    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    # end::is_over[]

    def legal_moves(self):
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)
        # These two moves are always legal.
        moves.append(Move.pass_turn())
        moves.append(Move.resign())

        return moves

    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        game_result = compute_game_result(self)
        return game_result.winner


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)  # 设置窗口大小（宽度，高度）
    pygame.display.set_caption("围棋")  # 设置标题

    draw_main_interface(screen)

    global game
    game = Game.new_game()
    bots = {
        Player.black: RandomBot(),
        Player.white: RandomBot(),
    }

    while True:
        if game_mode == 3:

            time.sleep(0.3)  # <1>

            bot_move = bots[game.next_player].select_move(game)
            game = game.apply_move(bot_move)
            draw_stones(game.board, screen)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    Handle_event(screen, event, bots)

        pygame.display.update()  # 刷新屏幕，显示更新


if __name__ == '__main__':
    main()
