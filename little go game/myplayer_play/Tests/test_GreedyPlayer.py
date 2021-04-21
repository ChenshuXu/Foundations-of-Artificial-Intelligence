from unittest import TestCase
from myplayer_play.Greedy.my_player3 import GreedyPlayer
from myplayer_play.Minmax.my_player3 import MinmaxPlayer
from myplayer_play.random_player import RandomPlayer
import myplayer_play.go as go
import myplayer_play.GameBoard as GameBoard

BLACK = 1
WHITE = 2


class TestGreedyPlayer(TestCase):
    def test_against_random(self):
        num = 10
        verbose = False
        my_player = GreedyPlayer(debug=False)
        print('Training MyPlayer against RandomPlayer for {} times......'.format(num))
        go.battle(my_player, RandomPlayer(), num, learn=True, show_result=True, verbose=verbose)
        go.battle(RandomPlayer(), my_player, num, learn=True, show_result=True, verbose=verbose)

    def test_against_minmax(self):
        num = 1
        verbose = False
        my_player = GreedyPlayer(debug=False)
        my_player2 = MinmaxPlayer(debug=False)
        print('Training MyPlayer against RandomPlayer for {} times......'.format(num))
        go.battle(my_player, my_player2, num, learn=True, show_result=True, verbose=verbose)
        go.battle(my_player2, my_player, num, learn=True, show_result=True, verbose=verbose)

    def test_evaluate1(self):
        # piece_type: 1('X')black or 2('O')white.
        piece_type = 2
        player = GreedyPlayer()
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board_int = GameBoard.encode_board(board)
        print(GameBoard.visualize_evaluation(board_int, piece_type))
        move = (2, 2)
        print(GameBoard.evaluate_move(board_int, piece_type, move, debug=True))

    def test_evaluate2(self):
        # piece_type: 1('X')black or 2('O')white.
        piece_type = 1
        player = GreedyPlayer()
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board_int = GameBoard.encode_board(board)
        print(GameBoard.visualize_evaluation(board_int, piece_type))
        move = (2, 2)
        print(GameBoard.evaluate_move(board_int, piece_type, move, debug=True))

    def test_evaluate3(self):
        # piece_type: 1('X')black or 2('O')white.
        piece_type = 1
        player = GreedyPlayer()
        board = [
            [0, 2, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 2, 0, 2, 2]
        ]
        board_int = GameBoard.encode_board(board)
        print(GameBoard.visualize_evaluation(board_int, piece_type))
