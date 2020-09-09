import copy

from goBoard import *
from Players import Player
from utils import Point, Move
from scoring import compute_game_result


class Game:
    def __init__(self, board, next_player, previous, move):
        self.board = board
        self.next_player = next_player
        self.previous_state = previous
        if self.previous_state is None:
            self.previous_states = frozenset()
        else:
            self.previous_states = frozenset(
                previous.previous_states |
                {(previous.next_player, previous.board.zobrist_hash())})
        self.last_move = move

    @classmethod
    def new_game(cls):
        board = Board(19, 19)
        return Game(board, Player.black, None, None)

    def apply_move(self, move):
        if move.is_play:
            next_board = copy.deepcopy(self.board)
            next_board.place_stone(self.next_player, move.point)

            return Game(next_board, self.next_player.other, self, move)
        elif move.is_restart or move.is_turn_back:
            return Game.new_game()
        elif move.is_regret:
            # print("try regret")
            last_turn = self.previous_state.previous_state
            return Game(last_turn.board, last_turn.next_player, last_turn.previous_state, last_turn.last_move)
        elif move.is_resign or move.is_pass:
            next_board = self.board
            return Game(next_board, self.next_player.other, self, move)

    def is_move_self_capture(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        new_string = next_board.get_go_string(move.point)
        return new_string.num_liberties == 0

    @property
    def situation(self):
        return self.next_player, self.board

    def does_move_violate_ko(self, player, move):
        if not move.is_play:
            return False
        next_board = copy.deepcopy(self.board)
        next_board.place_stone(player, move.point)
        next_situation = (player.other, next_board.zobrist_hash())
        return next_situation in self.previous_states

    def if_game_can_regret(self):
        if self is None or self.previous_state is None or self.previous_state.previous_state is None or self.previous_state.previous_state.previous_state is None:
            return False
        else:
            return True

    def is_valid_move(self, move):  # 操作是否有效
        if self.is_over():
            return False
        if move.is_regret and not self.if_game_can_regret() or self.is_over():
            return False
        elif move.is_regret and self.if_game_can_regret() and not self.is_over():
            return True
        if move.is_restart or move.is_pass or move.is_resign or move.is_turn_back:
            return True
        return (
                self.board.get(move.point) is None and
                not self.is_move_self_capture(self.next_player, move) and
                not self.does_move_violate_ko(self.next_player, move))

    def is_over(self):
        if self.last_move is None:
            return False
        if self.last_move.is_resign:
            return True
        second_last_move = self.previous_state.last_move
        if second_last_move is None:
            return False
        return self.last_move.is_pass and second_last_move.is_pass

    def legal_moves(self):  # 所有合法的操作
        moves = []
        for row in range(1, self.board.num_rows + 1):
            for col in range(1, self.board.num_cols + 1):
                move = Move.play(Point(row, col))
                if self.is_valid_move(move):
                    moves.append(move)

        moves.append(Move.pass_turn())
        moves.append(Move.resign())
        moves.append(Move.restart())
        moves.append(Move.turn_back())

        return moves

    def winner(self):
        if not self.is_over():
            return None
        if self.last_move.is_resign:
            return self.next_player
        game_result = compute_game_result(self)
        return game_result.winner
