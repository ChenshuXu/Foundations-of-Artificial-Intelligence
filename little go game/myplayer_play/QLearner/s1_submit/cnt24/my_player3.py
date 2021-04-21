import GameBoard as GameBoard
import FileHandler as FileHandler

BLACK = 1
WHITE = 2


# Black=1, White=2
class QLearningPlayer:
    def __init__(self, q_table=None, debug=False, params=None):
        if q_table is None:
            q_table = {}
        self.type = 'greedy'
        self.piece_type = None
        self.previous_board = None
        self.board = None
        self.debug = debug
        self.valid_moves = {}  # key:encoded state, value:dict of moves
        self.params = params

        self.q_table = q_table

        self.history = {}  # key: encoded state, value: calculated best move

    def get_input(self, piece_type, previous_board, board):
        """
        Get one input.

        :param piece_type: 1('X') or 2('O').
        :param previous_board: board int
        :param board: current board int
        :return: (row, column) coordinate of input.
        """
        board_int = GameBoard.encode_board(board)
        previous_board_int = GameBoard.encode_board(previous_board)
        self.previous_board = previous_board_int
        self.board = board_int
        self.piece_type = piece_type

        if piece_type == 1 and board_int == 0:
            return 2, 2

        if self.debug:
            print("=====player debug=====")
            print("{}'s move".format(self.piece_type))
        score, action = self._greedy(previous_board_int, board_int, "move")
        if self.debug:
            print(GameBoard.visualize_evaluation(board, piece_type))
            print("minmax player make action {} with score {}".format(action, score))
            print("=====player debug=====")
        return action

    def learn(self, result):
        pass

    def _greedy(self, previous_board_int, board_int, previous_action):
        valid_moves = self._get_valid_moves(previous_board_int, board_int, self.piece_type)
        if not valid_moves:
            # TODO: handle no valid move, or pass
            return 0, "PASS"
        # check q table
        check = self._check_q_table(board_int, valid_moves)
        if check:
            return check

        # check history table
        # encoded_board = board_int
        # check = self._check_encoded_state(encoded_board, self.piece_type)
        # if check:
        #     return check

        best_value, action = float("-inf"), None
        for move in valid_moves:
            value = GameBoard.evaluate_move(board_int, self.piece_type, move, params=self.params)
            if value > best_value:
                best_value, action = value, move

        if not valid_moves:
            # TODO: handle no valid move, or pass
            return 0, "PASS"

        # write to history dictionary
        # self._store_encoded_state(encoded_board, self.piece_type, best_value, action)
        return best_value, action

    def _check_q_table(self, board_int, valid_moves):
        # standarize board
        state = GameBoard.standarize_board(board_int, self.piece_type)
        # direct find
        if state in self.q_table:
            print("find")
            return self._find_max(self.q_table[state], valid_moves)

        # transform and search
        states = GameBoard.rotate_board(state)
        for s in states:
            if s in self.q_table:
                print("find in trans")
                return self._find_max(self.q_table[s], valid_moves)
        return False

    def _find_max(self, q_values, valid_moves):
        curr_max = float("-inf")
        move = None
        for i in range(5):
            for j in range(5):
                if (i, j) in valid_moves:
                    value = q_values[i][j]
                    if value > curr_max:
                        curr_max = value
                        move = (i,j)
        return curr_max, move

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

    def _get_valid_moves(self, previous_board_int, board_int, piece_type):
        moves = GameBoard.get_valid_moves(previous_board_int, board_int, piece_type)
        return moves


if __name__ == "__main__":
    piece_type, previous_board, board = FileHandler.readInput(5)
    q_table = FileHandler.readQTable()
    player = QLearningPlayer(q_table=q_table)
    action = player.get_input(piece_type, previous_board, board)
    # FileHandler.writeQTable(player.history)
    FileHandler.writeOutput(action)
