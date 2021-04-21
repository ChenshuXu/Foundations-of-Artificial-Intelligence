from copy import deepcopy

from myplayer_play.host import GO
from myplayer_play.Minmax.my_player3 import MinmaxPlayer
from myplayer_play.random_player import RandomPlayer
from myplayer_play.Greedy.my_player3 import GreedyPlayer


def readInput(n, path="input.txt"):
    piece_type = 1

    previous_board = [[0 for _ in range(5)] for _ in range(5)]
    board = [[0 for _ in range(5)] for _ in range(5)]

    return piece_type, previous_board, board


def play(go, player1, player2, learn):
    '''
    The game starts!

    :param go: the host instance.
    :param player1: Player instance.
    :param player2: Player instance.
    :param learn: if in learn mode.
    :return: piece type of winner of the game (0 if it's a tie).
    '''
    go.init_board(5)
    if player1.type == 'manual' or player2.type == 'manual':
        go.verbose = True
        print('----------Input "exit" to exit the program----------')
        print('X stands for black chess, O stands for white chess.')
        go.visualize_board()

    verbose = go.verbose
    result = -1
    game_over = False
    # Game starts!
    while not game_over:
        if go.X_move:
            piece_type = 1
        else:
            piece_type = 2
        # Judge if the game should end
        if go.game_end(piece_type):
            result = go.judge_winner()
            if verbose:
                print('Game ended.')
                if result == 0:
                    print('The game is a tie.')
                else:
                    print('The winner is {}'.format('X' if result == 1 else 'O'))
            game_over = True
            break

        if verbose:
            player = "X" if piece_type == 1 else "O"
            print(player + " makes move...")

        # Game continues
        previous_board = go.previous_board
        board = go.board
        if piece_type == 1:
            action = player1.get_input(piece_type, previous_board, board)
        else:
            action = player2.get_input(piece_type, previous_board, board)

        if verbose:
            player = "X" if piece_type == 1 else "O"
            print(action)

        if action != "PASS":
            # If invalid input, continue the loop. Else it places a chess on the board.
            if not go.place_chess(action[0], action[1], piece_type):
                if verbose:
                    go.visualize_board()
                continue

            go.died_pieces = go.remove_died_pieces(3 - piece_type)  # Remove the dead pieces of opponent
        else:
            go.previous_board = deepcopy(go.board)

        if verbose:
            go.visualize_board()  # Visualize the board again
            print()

        go.n_move += 1
        go.X_move = not go.X_move  # Players take turn

    if learn:
        player1.learn(result)
        player2.learn(result)

    return result


def battle(player1, player2, iter, learn=False, show_result=True, verbose=False):
    p1_stats = [0, 0, 0]  # draw, win, lose
    for i in range(0, iter):
        N = 5
        piece_type, previous_board, board = readInput(N, path="input.txt")
        go = GO(N)
        go.verbose = verbose
        go.set_board(piece_type, previous_board, board)
        result = play(go, player1, player2, learn)
        p1_stats[result] += 1

    p1_stats = [round(x / iter * 100.0, 1) for x in p1_stats]
    if show_result:
        print('_' * 60)
        print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0],
                                                                 p1_stats[2]).center(50))
        print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0],
                                                                 p1_stats[1]).center(50))
        print('_' * 60)
        print()

    return p1_stats


if __name__ == "__main__":
    NUM = 1
    verbose = True
    myPlayer = MinmaxPlayer(debug=verbose)
    greedyPlayer = GreedyPlayer()
    # train: play NUM games against players who only make random moves
    print('Training MyPlayer against RandomPlayer for {} times......'.format(NUM))
    battle(myPlayer, RandomPlayer(), NUM, learn=True, show_result=True, verbose=verbose)
    # battle(RandomPlayer(), myPlayer, NUM, learn=True, show_result=True, verbose=verbose)
    # print(myPlayer.history)
    # print(myPlayer.q_values)
    # battle(myPlayer, RandomPlayer(), 1000)
    # battle(RandomPlayer(), myPlayer, 1000)
    # battle(RandomPlayer(), RandomPlayer(), NUM, learn=False, show_result=True, verbose=verbose)
    # battle(RandomPlayer(), myPlayer, NUM, learn=False, show_result=True, verbose=verbose)
