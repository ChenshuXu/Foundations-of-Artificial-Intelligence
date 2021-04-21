import random
import sys
import numpy as np
from copy import deepcopy
import GameBoard as GameBoard

WIN_REWARD = 1.0
DRAW_REWARD = 0.5
LOSS_REWARD = 0.0


# Black=1, White=2
class MinmaxPlayer:
    def __init__(self, depth=2, debug=False):
        self.type = 'minmax'
        self.piece_type = None
        self.depth = depth
        self.previous_board = None
        self.board = None
        self.debug = debug
        # self.branching_factor = 10

        # below need to store in file
        self.history = {}  # key: encoded state, value: best move
        self.n_move = 0  # Trace the number of moves

    def get_input(self, piece_type, previous_board, board):
        """
        Get one input.

        :param piece_type: 1('X') or 2('O').
        :param previous_board: board
        :param board: current board
        :return: (row, column) coordinate of input.
        """
        # self.go.set_board(piece_type, previous_board, board)
        self.previous_board = previous_board
        self.board = board
        self.piece_type = piece_type

        if piece_type == 1 and GameBoard.is_initial_board(board):
            self.n_move = 1
            return 2, 2

        # set up depth
        if self.n_move <= 6:
            self.depth = 0
        elif 6 < self.n_move <= 12:
            self.depth = 0
        elif 12 < self.n_move <= 18:
            self.depth = 0
        else:
            self.depth = 0

        if self.debug:
            print("=====player debug=====")
            print("{}'s move, n_move={}, d={}".format(self.piece_type, self.n_move, self.depth))
        score, action = self._max(previous_board, board, "move", self.depth, float("-inf"), float("inf"))
        if self.debug:
            print(self._visualize_evaluation(board, piece_type))
            print("minmax player make action {} with score {}".format(action, score))
            print("=====player debug=====")
        self.n_move += 2
        return action

    def learn(self, result):
        pass

    def _max(self, previous_board, board, previous_action, depth, alpha, beta):
        # check history table
        if self._encode_state(board) in self.history:
            return self.history[self._encode_state(board)]

        # check game result
        """
        if game_board.game_end(previous_board, board, previous_action):
            result = game_board.judge_winner(board)
            if result == self.piece_type:
                # win
                return float("inf"), None
            elif result == 0:
                # will not happen
                return DRAW_REWARD, None
            else:
                # lose
                return float("-inf"), None
        """

        valid_moves = []
        for i in range(5):
            for j in range(5):
                if GameBoard.valid_place_check(previous_board, board, i, j, self.piece_type, test_check=True):
                    valid_moves.append((i, j))

        if not valid_moves:
            # TODO: handle no valid move, or pass
            return 0, "PASS"

        # random.shuffle(valid_moves)
        if depth < 1:
            # TODO: replace with evaluation function and best move
            # print(board)
            # print("max end of depth")
            best_value, action = float("-inf"), None
            for move in valid_moves:
                value = self._evaluate(board, self.piece_type, move)
                if value > best_value:
                    best_value, action = value, move
            self.history[self._encode_state(board)] = (best_value, action)
            return best_value, action

        best_value, action = float("-inf"), None
        for i, j in valid_moves:
            new_previous_board = deepcopy(board)
            # impossible to be unsuccessful
            new_board, success = GameBoard.place_chess(previous_board, board, i, j, self.piece_type)
            value, a = self._min(new_previous_board, new_board, previous_action, depth - 1, alpha, beta)
            if value > best_value or action is None:  # first action or find bigger value
                best_value, action = value, (i, j)
                self.history[self._encode_state(board)] = (best_value, action)
            # best_value = max(value, best_value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break

        return best_value, action

    def _min(self, previous_board, board, previous_action, depth, alpha, beta):
        opponent = 3 - self.piece_type
        # check history table
        if self._encode_state(board) in self.history:
            return self.history[self._encode_state(board)]

        # check game result
        """
        if game_board.game_end(previous_board, board, previous_action):
            result = game_board.judge_winner(board)
            if result == opponent:
                # win
                return float("inf"), None
            elif result == 0:
                # will not happen
                return DRAW_REWARD, None
            else:
                # lose
                return float("-inf"), None
        """

        valid_moves = []
        for i in range(5):
            for j in range(5):
                if GameBoard.valid_place_check(previous_board, board, i, j, opponent, test_check=True):
                    valid_moves.append((i, j))

        if not valid_moves:
            # TODO: handle no valid move, or pass
            return 0, "PASS"

        # random.shuffle(valid_moves)
        if depth < 1:
            best_value, action = float("inf"), None
            for move in valid_moves:
                value = self._evaluate(board, opponent, move)
                if value < best_value:
                    best_value, action = value, move
            self.history[self._encode_state(board)] = (best_value, action)
            return best_value, action

        best_value, action = float("inf"), None
        for i, j in valid_moves:
            new_previous_board = deepcopy(board)
            # impossible to be unsuccessful
            new_board, success = GameBoard.place_chess(previous_board, board, i, j, opponent)
            value, a = self._max(new_previous_board, new_board, previous_action, depth - 1, alpha, beta)
            if value < best_value or action is None:  # first action or find smaller value
                best_value, action = value, (i, j)
                self.history[self._encode_state(board)] = (best_value, action)
            # best_value = min(beta, best_value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break

        return best_value, action

    def _encode_state(self, board):
        # TODO: use Zobrist Hashing, https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-5-zobrist-hashing/
        return ''.join([str(board[i][j]) for i in range(5) for j in range(5)])

    def _filter_move(self, board, valid_moves):
        # TODO: can filter out less valuable moves
        new_moves = []
        for move in valid_moves:
            i, j = move
            neighbors = GameBoard.detect_neighbor_all(board, i, j)
            for nei_i, nei_j in neighbors:
                if board[nei_i][nei_j] != 0 and (nei_i, nei_j) in valid_moves:
                    new_moves.append((nei_i, nei_j))
        return valid_moves

    def _evaluate(self, board, piece_type, move, debug=False):
        """
        evaluate the score of this move
        input will always be a valid move

        :param board: the board
        :param piece_type: 1('X') or 2('O')
        :param move: (i, j)
        """
        i, j = move
        win_score = self._win_score(board, piece_type, move)
        kill_score = self._kill_enemy_score(board, piece_type, move)
        liberty_score = self._liberty_score(board, piece_type, move)
        connection_score = self._connecting_score(board, piece_type, move)
        edge_score = self._edge_score(board, move)
        if debug:
            print("on move ({},{}) win: {} kill: {} liberty: {} connection: {} edge: {}".format(
                i, j, win_score, kill_score, liberty_score, connection_score, edge_score))
        return win_score * 0.3 + kill_score * 8 + liberty_score * 0.1 + connection_score * 1.1 + edge_score * 0.3

    def _win_score(self, board, piece_type, move):
        """
        calculate who has higher score after this move
        positive if winning
        """
        i, j = move
        test_board = deepcopy(board)
        test_board[i][j] = piece_type
        # my score - opponents score
        score = GameBoard.score(test_board, piece_type) - GameBoard.score(test_board, 3 - piece_type)
        if piece_type == 2:
            score += 2.5
        return score

    def _kill_enemy_score(self, board, piece_type, move):
        """
        check this move will kill how many enemy stones

        :param board: the board
        :param piece_type: 1('X') or 2('O')
        :param move: (i, j)
        :return: count of killed enemy stones
        """
        i, j = move
        test_board = deepcopy(board)
        test_board[i][j] = piece_type
        died_pieces = GameBoard.find_died_pieces(test_board, 3 - piece_type)
        return len(died_pieces)

    def _liberty_score(self, board, piece_type, move):
        """
        check this move will increase how many liberty spaces

        :param board: the board
        :param piece_type: 1('X') or 2('O')
        :param move: (i, j)
        :return: count of liberty space
        """
        i, j = move
        after_board = deepcopy(board)
        after_board[i][j] = piece_type

        # find total liberty of previous board
        # previous_liberty = GameBoard.count_liberty(board, piece_type)
        after_liberty = GameBoard.count_liberty(after_board, piece_type)
        return after_liberty

    def _edge_score(self, board, move):
        """
        check if move is on edge, avoid move on the edge

        :param board: the board
        :param move: (i, j)
        :return: negative score if move on edge
        """
        i, j = move
        if 0 < i < 4 and 0 < j < 4:
            return 1
        else:
            return 0

    def _connecting_score(self, board, piece_type, move):
        """
        give connecting stones a positive score

        :param board: the board
        :param piece_type: 1('X') or 2('O')
        :param move: (i, j)
        :return: positive score if connect more stones
        """
        i, j = move
        connection_count = 0
        neighbors = GameBoard.detect_neighbor(board, i, j)
        for nei_i, nei_j in neighbors:
            if board[nei_i][nei_j] == piece_type:
                connection_count += 1
        return connection_count

    def _visualize_evaluation(self, board, piece_type):
        visualize_board = [[0 for x in range(5)] for y in range(5)]
        valid_moves = []
        for i in range(5):
            for j in range(5):
                if GameBoard.valid_place_check(board, board, i, j, piece_type, test_check=True):
                    valid_moves.append((i, j))

        s = '\n'
        s += '     j={:<4d}j={:<4d}j={:<4d}j={:<4d}j={:<4d}'.format(0, 1, 2, 3, 4)
        s += '\n'
        for i in range(5):
            for j in range(5):
                if j == 0:
                    s += "i={}".format(i)
                if board[i][j] == 0:
                    if (i, j) in valid_moves:
                        s += "{:6.2f}".format(self._evaluate(board, piece_type, (i, j), debug=True))
                    else:
                        s += '   .  '
                elif board[i][j] == 1:
                    s += '   X  '
                else:
                    s += '   O  '
            s += '\n'
        return s

def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]

        return piece_type, previous_board, board


def readOutput(path="output.txt"):
    with open(path, 'r') as f:
        position = f.readline().strip().split(',')

        if position[0] == "PASS":
            return "PASS", -1, -1

        x = int(position[0])
        y = int(position[1])

    return "MOVE", x, y


def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)


def writePass(path="output.txt"):
    with open(path, 'w') as f:
        f.write("PASS")


def writeNextInput(piece_type, previous_board, board, path="input.txt"):
    res = ""
    res += str(piece_type) + "\n"
    for item in previous_board:
        res += "".join([str(x) for x in item])
        res += "\n"

    for item in board:
        res += "".join([str(x) for x in item])
        res += "\n"

    with open(path, 'w') as f:
        f.write(res[:-1])


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    player = MinmaxPlayer()
    action = player.get_input(piece_type, previous_board, board)
    writeOutput(action)
