import enum
import pygame
import math
import random

import goBoard
from utils import Point, Move


def is_point_an_eye(board, point, color):
    if board.get(point) is not None:
        return False
    for neighbor in point.neighbors():
        if board.is_on_grid(neighbor):
            neighbor_color = board.get(neighbor)
            if neighbor_color != color:
                return False

    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color:
                friendly_corners += 1
        else:
            off_board_corners += 1
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    return friendly_corners >= 3


# define white player as 0
# define black player as 1

# 修正落子位置
def fix_stone_pos(pos):
    quotient_x = math.floor(pos[0] / 40)
    quotient_y = math.floor(pos[1] / 40)
    remainder_x = pos[0] % 40
    remainder_y = pos[1] % 40

    if remainder_x >= 20:
        quotient_x += 1
    if remainder_y >= 20:
        quotient_y += 1

    row = int(quotient_x)
    col = int(quotient_y)

    return row, col


class Player(enum.Enum):
    black = 0
    white = 1

    @property
    def other(self):
        return Player.black if self == Player.white else Player.white


class Human():
    def __init__(self):
        pass

    @staticmethod
    def go_strategy(pos):
        r, c = fix_stone_pos(pos)
        # print(r,c)
        stone = Point(row=r, col=c)
        return stone


class Agent:
    def __init__(self):
        pass

    def select_move(self, game_state):
        raise NotImplementedError()

    # end::agent[]

    def diagnostics(self):
        return {}


class RandomBot(Agent):
    def select_move(self, game_state):
        """Choose a random valid move that preserves our own eyes."""
        candidates = []
        for r in range(1, game_state.board.num_rows):
            for c in range(1, game_state.board.num_cols):
                candidate = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(candidate)) and \
                        not is_point_an_eye(game_state.board,
                                            candidate,
                                            game_state.next_player):
                    candidates.append(candidate)
        if not candidates:
            return Move.pass_turn()
        return Move.play(random.choice(candidates))
