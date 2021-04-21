import GameBoard as GameBoard


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
        self.valid_moves = {}  # key:encoded state, value:dict of moves

        # below need to store in file
        self.history = {}  # key: encoded state, value:dict of {piece: best move}

        # TODO: load from storage

    def get_input(self, piece_type, previous_board, board):
        """
        Get one input.

        :param piece_type: 1('X') or 2('O').
        :param previous_board: board
        :param board: current board
        :return: (row, column) coordinate of input.
        """
        board_int = GameBoard.encode_board(board)
        previous_board_int = GameBoard.encode_board(previous_board)
        self.previous_board = previous_board_int
        self.board = board_int
        self.piece_type = piece_type

        # First piece
        if piece_type == 1 and board_int == 0:
            # TODO: write something to storage
            return 2, 2

        # self._setup_depth(board)

        if self.debug:
            print("=====player debug=====")
            print("{}'s move, d={}".format(self.piece_type, self.depth))
        score, action = self._max(previous_board_int, board_int, "move")
        if self.debug:
            print(GameBoard.visualize_evaluation(board_int, piece_type))
            print("minmax player make action {} with score {}".format(action, score))
            print("=====player debug=====")

        # TODO: write something to storage
        return action

    def _setup_depth(self, board_int):
        """
        set up depth depending on number of moves
        """
        empty_space = GameBoard.count_empty(board_int)
        if empty_space <= 8:
            self.depth = 3
        elif 8 < empty_space <= 12:
            self.depth = 4
        elif 12 < empty_space <= 16:
            self.depth = 3
        elif 16 < empty_space <= 20:
            self.depth = 2
        else:
            self.depth = 2

    def learn(self, result):
        pass

    def _max(self, previous_board_int, board_int, previous_action):
        valid_moves = self._get_valid_moves(previous_board_int, board_int, self.piece_type)
        if not valid_moves:
            return 0, "pass"

        best_value = float("-inf")
        action = None
        for i, j in valid_moves:
            new_previous_board_int = board_int
            # impossible to be unsuccessful
            new_board_int, success = GameBoard.place_chess(previous_board_int, board_int, i, j, self.piece_type)
            score = self._minmax(False, new_previous_board_int, new_board_int, "move", self.depth - 1, float("-inf"),
                                 float("inf"), debug=False)
            if self.debug:
                print(GameBoard.visualize_evaluation(board_int, self.piece_type))
                print("     {},{} with score {}".format(str(i), str(j), score))
            if score > best_value:
                best_value = score
                action = (i, j)
        return best_value, action

    def _minmax(self, is_max, previous_board_int, board_int, previous_action, depth, alpha, beta, debug=False):
        if is_max:
            piece_type = self.piece_type
        else:
            piece_type = 3 - self.piece_type

        # TODO: check if end of game (both don't have valid moves), return +inf or -inf

        # check history table
        encoded_board = board_int
        check = self._check_encoded_state(encoded_board, piece_type)
        if check:
            return check

        valid_moves = self._get_valid_moves(previous_board_int, board_int, piece_type)

        if not valid_moves:
            # TODO: handle no valid move
            return 0

        best_value = float("-inf") if is_max else float("inf")
        if depth < 1:
            for move in self._get_valid_moves(previous_board_int, board_int, self.piece_type):
                score = GameBoard.evaluate_move(board_int, self.piece_type, move)
                if is_max:
                    best_value = max(score, best_value)
                else:
                    best_value = min(score, best_value)

            if debug:
                print("     in {} end".format("max" if is_max else "min"))
                print(GameBoard.visualize_evaluation(board_int, self.piece_type))
                print("     give {} with score {}".format("max" if is_max else "min", best_value))
            return best_value

        for i, j in valid_moves:
            new_previous_board_int = board_int
            # impossible to be unsuccessful
            new_board_int, success = GameBoard.place_chess(previous_board_int, board_int, i, j, piece_type)
            score = self._minmax(not is_max, new_previous_board_int, new_board_int, previous_action, depth - 1, alpha, beta)
            if is_max:
                best_value = max(score, best_value)
                alpha = max(alpha, best_value)

            else:
                best_value = min(score, best_value)
                beta = min(best_value, beta)

            if beta <= alpha:
                break

        if debug:
            print("     in {}".format("max" if is_max else "min"))
            print(GameBoard.visualize_evaluation(board_int, self.piece_type))
            print("     give {} with score {}".format("max" if is_max else "min", best_value))

        # write to history dictionary
        self._store_encoded_state(encoded_board, piece_type, best_value)
        return best_value

    def _check_encoded_state(self, encoded_board, piece_type):
        if encoded_board in self.history:
            if piece_type in self.history[encoded_board]:
                return self.history[encoded_board][piece_type]
        return False

    def _store_encoded_state(self, encoded_board, piece_type, value):
        if encoded_board in self.history:
            self.history[encoded_board][piece_type] = value
        else:
            self.history[encoded_board] = {piece_type: value}

    def _get_valid_moves(self, previous_board_int, board_int, piece_type):
        # state = self._encode_state(board)
        # if state in self.valid_moves:
        #     if piece_type in self.valid_moves[state]:
        #         return self.valid_moves[state][piece_type]

        moves = GameBoard.get_valid_moves(previous_board_int, board_int, piece_type)
        # self.valid_moves[state] = {piece_type: moves}
        return moves


def readInput(n, path="input.txt"):
    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n + 1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n + 1: 2 * n + 1]]

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
    player = MinmaxPlayer()
    action = player.get_input(piece_type, previous_board, board)

    return action


if __name__ == "__main__":
    action = load()
    writeOutput(action)
