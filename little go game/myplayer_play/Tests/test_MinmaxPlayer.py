from unittest import TestCase

from myplayer_play.Minmax.my_player3 import MinmaxPlayer
from myplayer_play.random_player import RandomPlayer
from myplayer_play.Greedy.my_player3 import GreedyPlayer
import myplayer_play.go as go

BLACK = 1
WHITE = 2

class TestMinmaxPlayer(TestCase):
    def test_against_random_player(self):
        num = 10
        verbose = True
        my_player = MinmaxPlayer(debug=True)
        print('Training MyPlayer against RandomPlayer for {} times......'.format(num))
        go.battle(my_player, RandomPlayer(), num, learn=True, show_result=True, verbose=verbose)
        go.battle(RandomPlayer(), my_player, num, learn=True, show_result=True, verbose=verbose)

    def test_random_first(self):
        num = 1
        verbose = True
        my_player = MinmaxPlayer(debug=False)
        print('Training MyPlayer against RandomPlayer for {} times......'.format(num))
        go.battle(RandomPlayer(), my_player, num, learn=True, show_result=True, verbose=verbose)

    def test_minmax_first(self):
        num = 1
        verbose = True
        my_player = MinmaxPlayer(debug=True)
        print('Training MyPlayer against RandomPlayer for {} times......'.format(num))
        go.battle(my_player, RandomPlayer(), num, learn=True, show_result=True, verbose=verbose)

    def test_against_greedy_first(self):
        num = 1
        verbose = True
        my_player2 = GreedyPlayer(debug=False)
        my_player = MinmaxPlayer(debug=False)
        print('Training MyPlayer against RandomPlayer for {} times......'.format(num))
        go.battle(my_player, my_player2, num, learn=True, show_result=True, verbose=verbose)

    def test_against_greedy_not_first(self):
        num = 1
        verbose = True
        my_player2 = GreedyPlayer(debug=False)
        my_player = MinmaxPlayer(debug=False)
        print('Training MyPlayer against RandomPlayer for {} times......'.format(num))
        go.battle(my_player2, my_player, num, learn=True, show_result=True, verbose=verbose)

    def test_get_input1(self):
        player = MinmaxPlayer(debug=True)
        piece_type = 1
        previous_board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board = [
            [0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        player.get_input(piece_type, previous_board, board)

    def test_get_input2(self):
        piece_type = 2
        p_board = [
            [0, 0, 0, 0, 0],
            [0, 1, 2, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 2, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board = [
            [0, 0, 0, 0, 0],
            [0, 1, 2, 0, 0],
            [1, 0, 1, 2, 0],
            [0, 1, 2, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        player = MinmaxPlayer(depth=1, debug=True)
        print(player.get_input(piece_type, p_board, board))

    def test_get_input3(self):
        piece_type = 1
        p_board = [
            [0, 0, 0, 2, 0],
            [2, 0, 2, 1, 1],
            [0, 2, 1, 0, 1],
            [0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        board = [
            [0, 0, 0, 2, 0],
            [2, 0, 2, 1, 1],
            [0, 2, 1, 0, 1],
            [0, 2, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        player = MinmaxPlayer(depth=3, debug=True)
        print(player.get_input(piece_type, p_board, board))

    def test_evaluate1(self):
        # piece_type: 1('X')black or 2('O')white.
        piece_type = 2
        player = MinmaxPlayer()
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        print(player._visualize_evaluation(board, piece_type))
        move = (2, 2)
        print(player._evaluate_move(board, piece_type, move, debug=True))


    def test_evaluate2(self):
        # piece_type: 1('X')black or 2('O')white.
        piece_type = 1
        player = MinmaxPlayer()
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        print(player._visualize_evaluation(board, piece_type))
        move = (2, 2)
        print(player._evaluate_move(board, piece_type, move, debug=True))


    def test_evaluate3(self):
        # piece_type: 1('X')black or 2('O')white.
        piece_type = 1
        player = MinmaxPlayer()
        board = [
            [0, 2, 0, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 2, 0, 2, 2]
        ]
        print(player._visualize_evaluation(board, piece_type))


    def test_evaluate_kill(self):
        # piece_type: 1('X')black or 2('O')white.
        piece_type = 2
        player = MinmaxPlayer(piece_type)
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 2, 0],
            [0, 0, 2, 1, 0],
            [0, 2, 0, 0, 0]
        ]
        print(player._visualize_evaluation(board, piece_type))

    def test_file_write(self):
        piece_type = 2
        p_board = [
            [0, 0, 0, 0, 0],
            [0, 1, 2, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 2, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board = [
            [0, 0, 0, 0, 0],
            [0, 1, 2, 0, 0],
            [1, 0, 1, 2, 0],
            [0, 1, 2, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        player = MinmaxPlayer(debug=True)
