import random
import sys
import numpy as np
from copy import deepcopy
import GameBoard as GameBoard


# Black=1, White=2
class GreedyPlayer:
    def __init__(self, depth=2, debug=False):
        self.type = 'minmax'
        self.piece_type = None
        self.depth = depth
        self.previous_board = None
        self.board = None
        self.debug = debug
        # self.branching_factor = 10
        self.valid_moves = {}  # key:encoded state, value:dict of moves

        # below need to store in file
        self.history = {}  # key: encoded state, value: best move

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
            return 2, 2

        if self.debug:
            print("=====player debug=====")
            print("{}'s move".format(self.piece_type))
        score, action = self._greedy(previous_board, board, "move")
        if self.debug:
            print(self._visualize_evaluation(board, piece_type))
            print("minmax player make action {} with score {}".format(action, score))
            print("=====player debug=====")
        return action

    def learn(self, result):
        pass

    def _greedy(self, previous_board, board, previous_action):
        # check history table
        encoded_board = self._encode_state(board)
        check = self._check_encoded_state(encoded_board, self.piece_type)
        if check:
            return check

        valid_moves = self._get_valid_moves(previous_board, board, self.piece_type)
        best_value, action = float("-inf"), None
        for move in valid_moves:
            value = self._evaluate_move(board, self.piece_type, move)
            if value > best_value:
                best_value, action = value, move

        if not valid_moves:
            # TODO: handle no valid move, or pass
            return 0, "PASS"

        # write to history dictionary
        self._store_encoded_state(encoded_board, self.piece_type, best_value, action)
        return best_value, action

    def _encode_state(self, board):
        # TODO: use Zobrist Hashing, https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-5-zobrist-hashing/
        return ''.join([str(board[i][j]) for i in range(5) for j in range(5)])

    def _check_encoded_state(self, encoded_board, piece_type):
        # return False
        if encoded_board in self.history:
            if piece_type in self.history[encoded_board]:
                return self.history[encoded_board][piece_type]
        return False

    def _store_encoded_state(self, encoded_board, piece_type, value, action):
        # pass
        if encoded_board in self.history:
            self.history[encoded_board][piece_type] = (value, action)
        else:
            self.history[encoded_board] = {piece_type: (value, action)}

    def _get_valid_moves(self, previous_board, board, piece_type):
        state = self._encode_state(board)
        if state in self.valid_moves:
            if piece_type in self.valid_moves[state]:
                return self.valid_moves[state][piece_type]

        moves = GameBoard.get_valid_moves(previous_board, board, piece_type)
        self.valid_moves[state] = {piece_type: moves}
        return moves

    def _evaluate_move(self, board, piece_type, move, debug=False):
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
            elif board[nei_i][nei_j] == 3-piece_type:
                connection_count += 0.6
        return connection_count

    def _visualize_evaluation(self, board, piece_type):
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
                        s += "{:6.2f}".format(self._evaluate_move(board, piece_type, (i, j), debug=True))
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

def read_self_store():
    pass


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


def load():
    """
    read input file and self storage
    """
    N = 5
    piece_type, previous_board, board = readInput(N)
    # history, n_move =
    player = GreedyPlayer()
    action = player.get_input(piece_type, previous_board, board)

    return action

if __name__ == "__main__":
    action = load()
    writeOutput(action)
