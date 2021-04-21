BLACK = 1
WHITE = 2


def score(board_int, piece_type):
    """
    Get score of a player by counting the number of stones.
    :return: boolean indicating whether the game should end.
    """
    cnt = 0
    for i in range(5):
        for j in range(5):
            if get_board_piece(board_int, i, j) == piece_type:
                cnt += 1
    return cnt


def count_empty(board_int):
    cnt = 0
    for i in range(5):
        for j in range(5):
            if get_board_piece(board_int, i, j) == 0:
                cnt += 1
    return cnt


def compare_board(board1, board2):
    for i in range(5):
        for j in range(5):
            if board1[i][j] != board2[i][j]:
                return False
    return True


def judge_winner(board_int):
    """
    Judge the winner of the game by number of pieces for each player.
    :return: piece type of winner of the game (0 if it's a tie).
    """
    cnt_1 = score(board_int, 1)
    cnt_2 = score(board_int, 2)
    if cnt_1 > cnt_2 + 2.5:
        return 1
    elif cnt_1 < cnt_2 + 2.5:
        return 2
    else:
        return 0


def game_end(previous_board_int, board_int, action="MOVE"):
    """
    Check if the game should end
    """
    if previous_board_int == board_int and action == "PASS":
        return True
    return False


def get_valid_moves(previous_board_int, board_int, piece_type):
    """
    Find out all valid moves for this piece type
    """
    valid_moves = []
    for i in range(5):
        for j in range(5):
            if valid_place_check(previous_board_int, board_int, i, j, piece_type, test_check=True):
                valid_moves.append((i, j))
    return valid_moves


def detect_neighbor_all(board_int, i, j):
    """
    Detect neighbors of a given stone in 8 directions

    :param board_int: board int
    :param i: row number of the board.
    :param j: column number of the board.
    :return: a list containing the neighbors row and column (row, column) of position (i, j).
    """
    neighbors = []
    if i > 0:
        neighbors.append((i - 1, j))
    if i < 4:
        neighbors.append((i + 1, j))
    if j > 0:
        neighbors.append((i, j - 1))
    if j < 4:
        neighbors.append((i, j + 1))
    if i > 0 and j > 0:
        neighbors.append((i - 1, j - 1))
    if i > 0 and j < 4:
        neighbors.append((i - 1, j + 1))
    if i < 4 and j > 0:
        neighbors.append((i + 1, j - 1))
    if i < 4 and j < 4:
        neighbors.append((i + 1, j + 1))
    return neighbors


def detect_neighbor(board_int, i, j):
    """
    Detect all the neighbors of a given stone.

    :param board_int: board int, not use
    :param i: row number of the board.
    :param j: column number of the board.
    :return: a list containing the neighbors row and column (row, column) of position (i, j).
    """
    neighbors = []
    # Detect borders and add neighbor coordinates
    if i > 0:
        neighbors.append((i - 1, j))
    if i < 4:
        neighbors.append((i + 1, j))
    if j > 0:
        neighbors.append((i, j - 1))
    if j < 4:
        neighbors.append((i, j + 1))
    return neighbors


def detect_neighbor_ally(board_int, i, j):
    """
    Detect the neighbor allies of a given stone.

    :param board_int: board int
    :param i: row number of the board.
    :param j: column number of the board.
    :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
    """
    neighbors = detect_neighbor(board_int, i, j)  # Detect neighbors
    group_allies = []
    # Iterate through neighbors
    for piece in neighbors:
        # Add to allies list if having the same color
        if get_board_piece(board_int, piece[0], piece[1]) == get_board_piece(board_int, i, j):
            group_allies.append(piece)
    return group_allies


def ally_dfs(board_int, i, j):
    """
    Using DFS to search for all allies of a given stone.

    :param i: row number of the board.
    :param j: column number of the board.
    :return: a list containing the all allies row and column (row, column) of position (i, j).
    """
    stack = [(i, j)]  # stack for DFS serach
    ally_members = []  # record allies positions during the search
    while stack:
        piece = stack.pop()
        ally_members.append(piece)
        neighbor_allies = detect_neighbor_ally(board_int, piece[0], piece[1])
        for ally in neighbor_allies:
            if ally not in stack and ally not in ally_members:
                stack.append(ally)
    return ally_members


def find_liberty(board_int, i, j):
    """
    Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

    :param board_int: board int
    :param i: row number of the board.
    :param j: column number of the board.
    :return: boolean indicating whether the given stone still has liberty.
    """
    ally_members = ally_dfs(board_int, i, j)
    for member in ally_members:
        neighbors = detect_neighbor(board_int, member[0], member[1])
        for piece in neighbors:
            # If there is empty space around a piece, it has liberty
            if get_board_piece(board_int, piece[0], piece[1]) == 0:
                return True
    # If none of the pieces in a allied group has an empty space, it has no liberty
    return False


def count_liberty(board_int, piece_type):
    """
    Count how many liberty of a given piece type

    :param board_int: the game board
    :param piece_type: 1('X') or 2('O')
    :return: size of liberty
    """
    count = 0
    all_neighbors = set()
    for i in range(5):
        for j in range(5):
            if get_board_piece(board_int, i, j) == piece_type:
                # check 4 directions, see if have liberty
                neighbors = detect_neighbor(board_int, i, j)
                for nei in neighbors:
                    all_neighbors.add(nei)
    for nei_i, nei_j in all_neighbors:
        if get_board_piece(board_int, nei_i, nei_j) == 0:
            count += 1
    return count


def find_died_pieces(board_int, piece_type):
    """
    Find the died stones that has no liberty in the board for a given piece type.

    :param board_int: board int
    :param piece_type: 1('X') or 2('O').
    :return: a list containing the dead pieces row and column(row, column).
    """
    died_pieces = []

    for i in range(5):
        for j in range(5):
            # Check if there is a piece at this position:
            if get_board_piece(board_int, i, j) == piece_type:
                # The piece die if it has no liberty
                if not find_liberty(board_int, i, j):
                    died_pieces.append((i, j))
    return died_pieces


def remove_certain_pieces(board_int, positions):
    """
    Remove the stones of certain locations.

    :param positions: a list containing the pieces to be removed row and column(row, column)
    :return: None.
    """
    for piece in positions:
        board_int = new_board(board_int, piece[0], piece[1], 0)
    return board_int


def remove_died_pieces(board_int, piece_type):
    """
    Remove the dead stones in the board.

    :param piece_type: 1('X') or 2('O').
    :return: locations of dead pieces, new board
    """

    died_pieces = find_died_pieces(board_int, piece_type)
    if not died_pieces:
        return [], board_int
    new_board_int = remove_certain_pieces(board_int, died_pieces)
    return died_pieces, new_board_int


def valid_place_check(previous_board_int, board_int, i, j, piece_type, test_check=False):
    """
    Check whether a placement is valid.

    :param i: row number of the board.
    :param j: column number of the board.
    :param piece_type: 1(white piece) or 2(black piece).
    :param test_check: boolean if it's a test check.
    :return: boolean indicating whether the placement is valid.
    """
    verbose = True
    if test_check:
        verbose = False

    # Check if the place is in the board range
    if not (0 <= i < 5):
        if verbose:
            print('Invalid placement. row should be in the range 1 to {}.'.format(5 - 1))
        return False
    if not (0 <= j < 5):
        if verbose:
            print('Invalid placement. column should be in the range 1 to {}.'.format(5 - 1))
        return False

    # Check if the place already has a piece
    if get_board_piece(board_int, i, j) != 0:
        if verbose:
            print('Invalid placement. There is already a chess in this position.')
        return False

    # Copy the board for testing
    # Check if the place has liberty
    test_board_int = new_board(board_int, i, j, piece_type)
    if find_liberty(test_board_int, i, j):
        return True

    # If not, remove the died pieces of opponent and check again
    died_pieces, test_board_int = remove_died_pieces(test_board_int, 3 - piece_type)
    if not find_liberty(test_board_int, i, j):
        if verbose:
            print('Invalid placement. No liberty found in this position.')
        return False

    # Check special case: repeat placement causing the repeat board state (KO rule)
    else:
        if died_pieces and previous_board_int == test_board_int:
            if verbose:
                print('Invalid placement. A repeat move not permitted by the KO rule.')
            return False
    return True


def place_chess(previous_board_int, board_int, i, j, piece_type):
    """
    Place a chess stone in the board.

    :param i: row number of the board.
    :param j: column number of the board.
    :param piece_type: 1('X') or 2('O').
    :return: boolean indicating whether the placement is valid.
    """

    valid_place = valid_place_check(previous_board_int, board_int, i, j, piece_type)
    if not valid_place:
        return None, False
    new_b_int = new_board(board_int, i, j, piece_type)
    return new_b_int, True


def visualize_board_list(board):
    s = '\n'
    s += '-' * len(board) * 2
    s += '\n'
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                s += '. '
            elif board[i][j] == 1:
                s += 'X '
            else:
                s += 'O '
        s += '\n'
    s += '-' * len(board) * 2
    return s


def visualize_board(board_int):
    """
    Visualize the board.

    :return: None
    """
    board = decode_board(board_int)
    s = '\n'
    s += '-' * len(board) * 2
    s += '\n'
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                s += '. '
            elif board[i][j] == 1:
                s += 'X '
            else:
                s += 'O '
        s += '\n'
    s += '-' * len(board) * 2
    return s


def evaluate_board(previous_board_int, board_int, piece_type, debug=False):
    """
    evaluate score of this board
    """
    s = score(board_int, piece_type) - score(board_int, 3 - piece_type)
    if piece_type == 2:
        s += 2.5
    return s


def evaluate_move(board_int, piece_type, move, debug=False,
                  params=None):
    """
    evaluate the score of this move
    input will always be a valid move

    :param board_int: board int
    :param piece_type: 1('X') or 2('O')
    :param move: (i, j)
    """
    if params is None:
        params = [0.3, 8, 2, 10, 0.1, 1, 0.1]
    win_s = win_score(board_int, piece_type, move)
    kill_s = kill_enemy_score(board_int, piece_type, move)
    kill_s2 = kill_enemy_score2(board_int, piece_type, move)
    be_killed_s = be_killed_score(board_int, piece_type, move)
    liberty_s = liberty_score(board_int, piece_type, move)
    connection_score = connecting_score(board_int, piece_type, move)
    edge_s = edge_score(board_int, move)
    # if debug:
    #     print("on move ({},{}) win: {} kill: {} liberty: {} connection: {} edge: {}".format(
    #         i, j, win_score, kill_score, liberty_score, connection_score, edge_score))
    return win_s * 0.3 + kill_s * 8 + kill_s2 * 2 + be_killed_s * 10 + liberty_s * 2 + connection_score * 1 + edge_s * 0.1


def win_score(board_int, piece_type, move):
    """
    calculate who has higher score after this move
    positive if winning
    """
    i, j = move
    test_board_int = new_board(board_int, i, j, piece_type)

    # my score - opponents score
    s = score(test_board_int, piece_type) - score(test_board_int, 3 - piece_type)
    if piece_type == 2:
        s += 2.5
    return s


def kill_enemy_score(board_int, piece_type, move):
    """
    check this move will kill how many enemy stones in 1 move

    :param board_int: board int
    :param piece_type: 1('X') or 2('O')
    :param move: (i, j), must be a valid move
    :return: count of killed enemy stones
    """
    i, j = move
    test_board_int = new_board(board_int, i, j, piece_type)

    died_pieces = find_died_pieces(test_board_int, 3 - piece_type)
    return len(died_pieces)


def kill_enemy_score2(board_int, piece_type, move):
    """
    check this move will kill how many enemy stones in 2 moves

    :param board_int: board int
    :param piece_type: 1('X') or 2('O')
    :param move: (i, j), must be a valid move
    :return: count of killed enemy stones
    """
    i, j = move
    test_board_int = new_board(board_int, i, j, piece_type)
    valid_moves = get_valid_moves(board_int, test_board_int, piece_type)
    max_kill = 0
    for move in valid_moves:
        kill_cnt = kill_enemy_score(test_board_int, piece_type, move)
        if kill_cnt > max_kill:
            max_kill = kill_cnt

    return max_kill


def be_killed_score(board_int, piece_type, move):
    """
    penalty if enemy can kill this stone after 1 step

    :param board_int: the board
    :param piece_type: 1('X') or 2('O')
    :param move: (i, j), must be a valid move
    :return: -1 for being killed, 0 for not being killed
    """
    all_died_pieces = set()
    i, j = move
    board_copy = new_board(board_int, i, j, piece_type)
    valid_moves = get_valid_moves(board_int, board_copy, 3 - piece_type)
    for k, l in valid_moves:
        test_board_int = new_board(board_copy, k, l, 3 - piece_type)
        died_pieces = find_died_pieces(test_board_int, piece_type)
        for piece in died_pieces:
            all_died_pieces.add(piece)
    if (i, j) in all_died_pieces:
        return -1
    return 0


def liberty_score(board_int, piece_type, move):
    """
    check this move will increase how many liberty spaces

    :param board_int: the board
    :param piece_type: 1('X') or 2('O')
    :param move: (i, j)
    :return: count of liberty space
    """
    i, j = move
    test_board_int = new_board(board_int, i, j, piece_type)

    opponent_liberty = count_liberty(board_int, 3-piece_type)
    my_liberty = count_liberty(test_board_int, piece_type)
    difference = my_liberty - opponent_liberty
    if difference < 5:
        return difference
    else:
        return 1


def edge_score(board_int, move):
    """
    check if move is on edge, avoid move on the edge

    :param board_int: the board
    :param move: (i, j)
    :return: negative score if move on edge
    """
    i, j = move
    if 0 < i < 4 and 0 < j < 4:
        return 1
    else:
        return 0


def connecting_score(board_int, piece_type, move):
    """
    give connecting stones a positive score

    :param board_int: board int
    :param piece_type: 1('X') or 2('O')
    :param move: (i, j)
    :return: positive score if connect more stones
    """
    # board = decode_board(board_int)
    i, j = move
    connection_count = 0
    neighbors = detect_neighbor(board_int, i, j)
    for nei_i, nei_j in neighbors:
        if get_board_piece(board_int, nei_i, nei_j) == piece_type:
            # connection_count += 1
            return 1
    return connection_count


def visualize_evaluation(board_int, piece_type):
    board = decode_board(board_int)
    valid_moves = []
    for i in range(5):
        for j in range(5):
            if valid_place_check(board_int, board_int, i, j, piece_type, test_check=True):
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
                    s += "{:6.2f}".format(evaluate_move(board_int, piece_type, (i, j), debug=True))
                else:
                    s += '   .  '
            elif board[i][j] == 1:
                s += '   X  '
            else:
                s += '   O  '
        s += '\n'
    return s


def encode_state(board):
    # TODO: use Zobrist Hashing, https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-5-zobrist-hashing/
    return encode_board(board)


def get_board_piece(board_int, i, j):
    """
    return piece on that position
    """
    shift = 50 - (i * 5 + j + 1) * 2
    mask = 3
    return board_int >> shift & mask


def update_board(board_int, i, j, piece_type):
    """
    directly change board int
    """
    shift = 50 - (i * 5 + j + 1) * 2
    value = piece_type << shift
    board_int |= value


def new_board(board_int, i, j, piece_type):
    """
    return new board after manipulation
    TODO: currently no 01->10 and no 10->01
    """
    shift = 50 - (i * 5 + j + 1) * 2
    # 01 or 10 to 00
    if piece_type == 0:
        # get that 2 bits, then XOR
        original_piece = board_int >> shift & 0b11
        original_piece = original_piece << shift
        return board_int ^ original_piece

    # 00 to 01 or 10
    shift = 50 - (i * 5 + j + 1) * 2
    value = piece_type << shift
    new_h = board_int | value
    return new_h


def encode_board(board):
    """
    convert 5*5 board to 25 bit int
    01 = 1
    10 = 2
    00 = 0
    """
    h = 0
    for i in range(5):
        for j in range(5):
            piece = board[i][j]
            h = h << 2
            h |= piece
    return h


def decode_board(h):
    """
    convert hash to board list
    """
    board = [[0 for _ in range(5)] for _ in range(5)]
    mask = 3  # 11
    for i in range(4, -1, -1):
        for j in range(4, -1, -1):
            test = h & mask
            board[i][j] = test
            h = h >> 2
    return board


def rotate_board(board_int):
    board = decode_board(board_int)
    other_boards_int = []
    for _ in range(3):
        rotate(board)
        other_boards_int.append(encode_board(board))
    return other_boards_int


def rotate(matrix):
    """
    modify matrix in-place instead.
    """
    n = 5
    for i in range(n // 2 + n % 2):
        for j in range(n // 2):
            tmp = matrix[n - 1 - j][i]
            matrix[n - 1 - j][i] = matrix[n - 1 - i][n - j - 1]
            matrix[n - 1 - i][n - j - 1] = matrix[j][n - 1 - i]
            matrix[j][n - 1 - i] = matrix[i][j]
            matrix[i][j] = tmp


def flip_board(board_int):
    """
    flip board left-right and up-down
    """
    pass


def standarize_board(board_int, piece_type):
    """
    if piece type is black/1/X no need to change
    if piece type is white/2/O change all white to black, all black to white
    """
    if piece_type == BLACK:
        return board_int

    for i in range(5):
        for j in range(5):
            piece = get_board_piece(board_int, i, j)
            if piece != 0:
                board_int = new_board(board_int, i, j, 0)
                board_int = new_board(board_int, i, j, 3-piece)
    return board_int