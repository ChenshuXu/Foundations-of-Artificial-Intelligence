from unittest import TestCase
from myplayer_play.Greedy.my_player3 import GreedyPlayer
from myplayer_play.Minmax.my_player3 import MinmaxPlayer
from myplayer_play.random_player import RandomPlayer
from myplayer_play.QLearner.my_player3 import QLearningPlayer
import myplayer_play.go as go
import myplayer_play.GameBoard as GameBoard
import myplayer_play.FileHandler as FileHandler

BLACK = 1
WHITE = 2


class TestQLearningPlayer(TestCase):
    def test_against_random(self):
        num = 100
        verbose = False
        q_table = FileHandler.read_q_table(path="../QLearner/QTable.pkl")
        my_player = QLearningPlayer(q_table=q_table, debug=False)
        print('Training MyPlayer against RandomPlayer for {} times......'.format(num))
        go.battle(my_player, RandomPlayer(), num, learn=True, show_result=True, verbose=verbose)
        go.battle(RandomPlayer(), my_player, num, learn=True, show_result=True, verbose=verbose)

    def test_against_greedy(self):
        num = 10
        verbose = False
        q_table = FileHandler.read_q_table(path="../QLearner/QTable.pkl")
        my_player = QLearningPlayer(q_table=q_table, debug=False)
        my_player2 = GreedyPlayer(debug=False)
        print('Training MyPlayer against Greedy player for {} times......'.format(num))
        go.battle(my_player, my_player2, num, learn=True, show_result=True, verbose=verbose)
        go.battle(my_player2, my_player, num, learn=True, show_result=True, verbose=verbose)

    def test_against_self(self):
        num = 100
        verbose = False
        q_table = FileHandler.read_q_table(path="../QLearner/QTable.pkl")
        my_player = QLearningPlayer(q_table=q_table, debug=False)
        my_player2 = QLearningPlayer(q_table=q_table, debug=False)
        print('Training MyPlayer against Greedy player for {} times......'.format(num))
        go.battle(my_player, my_player2, num, learn=True, show_result=True, verbose=verbose)
        go.battle(my_player2, my_player, num, learn=True, show_result=True, verbose=verbose)

    def test_evaluation(self):
        verbose = True
        q_table = FileHandler.read_q_table(path="../QLearner/QTable.pkl")
        my_player = QLearningPlayer(q_table=q_table, debug=False)
        previous_board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        previous_board_int = GameBoard.encode_board(previous_board)
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board_int = GameBoard.encode_board(board)
        valid_moves = GameBoard.get_valid_moves(previous_board_int, board_int, 2)
        print(my_player._check_q_table(board_int, valid_moves))
        print(my_player.get_input(2, previous_board, board))
