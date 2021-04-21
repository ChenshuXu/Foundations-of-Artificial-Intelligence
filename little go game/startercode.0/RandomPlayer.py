# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (default, Jul 16 2020, 14:00:26)
# [GCC 9.3.0]
# Embedded file name: /Users/bo/Documents/projects/561/TA Spring 2020/QL-Example-For-TicTacToe/RandomPlayer.py
# Compiled at: 2020-01-30 16:30:12
# Size of source mod 2**32: 661 bytes
from Board import Board
import numpy as np

class RandomPlayer:

    def __init__(self, side=None):
        self.side = side

    def set_side(self, side):
        self.side = side

    def move(self, board):
        if board.game_over():
            return
        else:
            candidates = []
            for i in range(0, 3):
                for j in range(0, 3):
                    if board.state[i][j] == 0:
                        candidates.append(tuple([i, j]))

            idx = np.random.randint(len(candidates))
            random_move = candidates[idx]
            return board.move(random_move[0], random_move[1], self.side)

    def learn(self, board):
        pass
# okay decompiling RandomPlayer.pyc