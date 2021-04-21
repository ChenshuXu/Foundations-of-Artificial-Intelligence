import myplayer_play.GameBoard as GameBoard


# Black=1, White=2
class GreedyPlayer:
    def __init__(self, debug=False):
        self.type = 'minmax'
        self.piece_type = None
        self.previous_board = None
        self.board = None
        self.debug = debug
        self.valid_moves = {}  # key:encoded state, value:dict of moves

        # below need to store in file
        self.history = {}  # key: encoded state, value: best move

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
        # check history table
        encoded_board = board_int
        check = self._check_encoded_state(encoded_board, self.piece_type)
        if check:
            return check

        valid_moves = self._get_valid_moves(previous_board_int, board_int, self.piece_type)
        best_value, action = float("-inf"), None
        for move in valid_moves:
            value = GameBoard.evaluate_move(board_int, self.piece_type, move)
            if value > best_value:
                best_value, action = value, move

        if not valid_moves:
            # TODO: handle no valid move, or pass
            return 0, "PASS"

        # write to history dictionary
        self._store_encoded_state(encoded_board, self.piece_type, best_value, action)
        return best_value, action

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
