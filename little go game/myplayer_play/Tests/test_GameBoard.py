from unittest import TestCase
import myplayer_play.GameBoard as GameBoard

BLACK = 1
WHITE = 2


class TestGameBoard(TestCase):

    def test_be_killed_score(self):
        piece_type = 2
        move = (2, 3)
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board_int = GameBoard.encode_board(board)
        result = GameBoard.be_killed_score(board_int, piece_type, move)
        self.assertEqual(result, -1)

        piece_type = 2
        move = (4, 2)
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 2, 2, 0, 0],
            [0, 0, 1, 1, 0],
            [0, 1, 0, 2, 0]
        ]
        board_int = GameBoard.encode_board(board)
        result = GameBoard.be_killed_score(board_int, piece_type, move)
        self.assertEqual(result, -1)

        piece_type = 2
        move = (1, 1)
        board = [
            [0, 0, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        board_int = GameBoard.encode_board(board)
        result = GameBoard.be_killed_score(board_int, piece_type, move)
        self.assertEqual(result, 0)

    def test_compute_hash(self):
        board = [
            [0, 1, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]
        hash = GameBoard.encode_board(board)
        print("hash is: {}".format(hash))
        res = GameBoard.decode_board(hash)
        print(GameBoard.visualize_board_list(res))
        self.assertTrue(GameBoard.compare_board(board, res))

    def test_new_board(self):
        board = [
            [0, 1, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]

        h = GameBoard.encode_board(board)
        new_b = [
            [0, 1, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]
        print(GameBoard.visualize_board_list(board))
        print(GameBoard.visualize_board_list(new_b))
        new_hash = GameBoard.new_board(h, 2, 1, 1)
        res = GameBoard.decode_board(new_hash)
        print(GameBoard.visualize_board_list(res))
        self.assertTrue(GameBoard.compare_board(res, new_b))

    def test_new_board2(self):
        board = [
            [0, 1, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]

        h = GameBoard.encode_board(board)
        new_b = [
            [0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]
        print(GameBoard.visualize_board_list(board))
        print(GameBoard.visualize_board_list(new_b))
        new_hash = GameBoard.new_board(h, 1, 2, 0)
        res = GameBoard.decode_board(new_hash)
        print(GameBoard.visualize_board_list(res))
        self.assertTrue(GameBoard.compare_board(res, new_b))

    def test_get_board_piece(self):
        board = [
            [0, 1, 0, 0, 0],
            [0, 0, 2, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]

        h = GameBoard.encode_board(board)
        self.assertEqual(GameBoard.get_board_piece(h, 0, 1), 1)
        self.assertEqual(GameBoard.get_board_piece(h, 4, 4), 2)
        self.assertEqual(GameBoard.get_board_piece(h, 1, 2), 2)

    def test_remove_died_pieces(self):
        board = [
            [0, 1, 1, 0, 0],
            [0, 1, 2, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]
        new_b = [
            [0, 1, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]
        board_int = GameBoard.encode_board(board)
        pieces, board_int = GameBoard.remove_died_pieces(board_int, 2)
        print(pieces)
        print(GameBoard.visualize_board(board_int))
        self.assertEqual(GameBoard.compare_board(new_b, GameBoard.decode_board(board_int)), True)
        self.assertEqual(GameBoard.encode_board(new_b), board_int)

    def test_standarize_board(self):
        board = [
            [0, 1, 1, 0, 0],
            [0, 1, 2, 1, 0],
            [0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 2]
        ]
        board_int = GameBoard.encode_board(board)
        new_board_int = GameBoard.standarize_board(board_int, WHITE)
        print(GameBoard.visualize_board(new_board_int))
        res_board = [
            [0, 2, 2, 0, 0],
            [0, 2, 1, 2, 0],
            [0, 0, 2, 0, 2],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 1]
        ]
        res_board_int = GameBoard.encode_board(res_board)
        self.assertEqual(new_board_int, res_board_int)

    def test_valid_place_check(self):
        pass

    def test_detect_neighbor_all(self):
        print(GameBoard.detect_neighbor_all(0, 4, 4))