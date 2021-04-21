from copy import deepcopy


def score(board, piece_type):
    """
    Get score of a player by counting the number of stones.
    :return: boolean indicating whether the game should end.
    """
    cnt = 0
    for i in range(5):
        for j in range(5):
            if board[i][j] == piece_type:
                cnt += 1
    return cnt


def judge_winner(board):
    """
    Judge the winner of the game by number of pieces for each player.
    :return: piece type of winner of the game (0 if it's a tie).
    """
    cnt_1 = score(board, 1)
    cnt_2 = score(board, 2)
    if cnt_1 > cnt_2 + 2.5:
        return 1
    elif cnt_1 < cnt_2 + 2.5:
        return 2
    else:
        return 0


def is_initial_board(board):
    for i in range(5):
        for j in range(5):
            if board[i][j] != 0:
                return False
    return True


def compare_board(board1, board2):
    for i in range(5):
        for j in range(5):
            if board1[i][j] != board2[i][j]:
                return False
    return True


def game_end(previous_board, board, action="MOVE"):
    """
    Check if the game should end
    """
    if compare_board(previous_board, board) and action == "PASS":
        return True
    return False

def get_valid_moves(previous_board, board, piece_type):
    """
    Find out all valid moves for this piece type
    """
    valid_moves = []
    for i in range(5):
        for j in range(5):
            if valid_place_check(previous_board, board, i, j, piece_type, test_check=True):
                valid_moves.append((i, j))
    return valid_moves

def detect_neighbor_all(board, i, j):
    """
    Detect neighbors of a given stone in 8 directions

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


def detect_neighbor(board, i, j):
    """
    Detect all the neighbors of a given stone.

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


def detect_neighbor_ally(board, i, j):
    """
    Detect the neighbor allies of a given stone.

    :param i: row number of the board.
    :param j: column number of the board.
    :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
    """
    neighbors = detect_neighbor(board, i, j)  # Detect neighbors
    group_allies = []
    # Iterate through neighbors
    for piece in neighbors:
        # Add to allies list if having the same color
        if board[piece[0]][piece[1]] == board[i][j]:
            group_allies.append(piece)
    return group_allies


def ally_dfs(board, i, j):
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
        neighbor_allies = detect_neighbor_ally(board, piece[0], piece[1])
        for ally in neighbor_allies:
            if ally not in stack and ally not in ally_members:
                stack.append(ally)
    return ally_members


def find_liberty(board, i, j):
    """
    Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

    :param i: row number of the board.
    :param j: column number of the board.
    :return: boolean indicating whether the given stone still has liberty.
    """
    ally_members = ally_dfs(board, i, j)
    for member in ally_members:
        neighbors = detect_neighbor(board, member[0], member[1])
        for piece in neighbors:
            # If there is empty space around a piece, it has liberty
            if board[piece[0]][piece[1]] == 0:
                return True
    # If none of the pieces in a allied group has an empty space, it has no liberty
    return False


def count_liberty(board, piece_type):
    """
    Count how many liberty of a given piece type

    :param board: the game board
    :param piece_type: 1('X') or 2('O')
    :return: size of liberty
    """
    count = 0
    all_neighbors = set()
    for i in range(5):
        for j in range(5):
            if board[i][j] == piece_type:
                # check 4 directions, see if have liberty
                neighbors = detect_neighbor(board, i, j)
                for nei in neighbors:
                    all_neighbors.add(nei)
    for nei_i, nei_j in all_neighbors:
        if board[nei_i][nei_j] == 0:
            count += 1
    return count


def find_died_pieces(board, piece_type):
    """
    Find the died stones that has no liberty in the board for a given piece type.

    :param piece_type: 1('X') or 2('O').
    :return: a list containing the dead pieces row and column(row, column).
    """
    died_pieces = []

    for i in range(len(board)):
        for j in range(len(board)):
            # Check if there is a piece at this position:
            if board[i][j] == piece_type:
                # The piece die if it has no liberty
                if not find_liberty(board, i, j):
                    died_pieces.append((i, j))
    return died_pieces


def remove_certain_pieces(board, positions):
    """
    Remove the stones of certain locations.

    :param positions: a list containing the pieces to be removed row and column(row, column)
    :return: None.
    """
    for piece in positions:
        board[piece[0]][piece[1]] = 0
    return board


def remove_died_pieces(board, piece_type):
    """
    Remove the dead stones in the board.

    :param piece_type: 1('X') or 2('O').
    :return: locations of dead pieces, new board
    """

    died_pieces = find_died_pieces(board, piece_type)
    if not died_pieces:
        return [], board
    new_board = remove_certain_pieces(board, died_pieces)
    return died_pieces, new_board


def valid_place_check(previous_board, board, i, j, piece_type, test_check=False):
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
    if not (0 <= i < len(board)):
        if verbose:
            print('Invalid placement. row should be in the range 1 to {}.'.format(len(board) - 1))
        return False
    if not (0 <= j < len(board)):
        if verbose:
            print('Invalid placement. column should be in the range 1 to {}.'.format(len(board) - 1))
        return False

    # Check if the place already has a piece
    if board[i][j] != 0:
        if verbose:
            print('Invalid placement. There is already a chess in this position.')
        return False

    # Copy the board for testing
    test_board = deepcopy(board)

    # Check if the place has liberty
    test_board[i][j] = piece_type
    if find_liberty(test_board, i, j):
        return True

    # If not, remove the died pieces of opponent and check again
    died_pieces, test_board = remove_died_pieces(test_board, 3 - piece_type)
    if not find_liberty(test_board, i, j):
        if verbose:
            print('Invalid placement. No liberty found in this position.')
        return False

    # Check special case: repeat placement causing the repeat board state (KO rule)
    else:
        if died_pieces and compare_board(previous_board, test_board):
            if verbose:
                print('Invalid placement. A repeat move not permitted by the KO rule.')
            return False
    return True


def place_chess(previous_board, board, i, j, piece_type):
    """
    Place a chess stone in the board.

    :param i: row number of the board.
    :param j: column number of the board.
    :param piece_type: 1('X') or 2('O').
    :return: boolean indicating whether the placement is valid.
    """

    valid_place = valid_place_check(previous_board, board, i, j, piece_type)
    if not valid_place:
        return None, False
    new_board = deepcopy(board)
    new_board[i][j] = piece_type
    return new_board, True


def visualize_board(board):
    """
    Visualize the board.

    :return: None
    """
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