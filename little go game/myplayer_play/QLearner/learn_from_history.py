import myplayer_play.GameBoard as GameBoard
import myplayer_play.FileHandler as FileHandler
import numpy as np

BLACK = 1
WHITE = 2

WIN_REWARD = 1.0
LOSS_REWARD = 0.0


def read_stage1_log(path, win_table, lose_table, aggressive_only=True):
    with open(path, "r") as f:
        lines = f.readlines()
        i = 0
        previous_board_int = 0
        board_int = 0
        black_board_list = []
        white_board_list = []
        champion_black_board_list = []
        champion_white_board_list = []
        winner = None
        start_play = False
        champion_player = False

        while i < len(lines):
            line = lines[i].strip()
            if "ERROR" in line or "not found or invalid format" in line:
                print("ERROR")
                break
            if "Invalid" in line:
                print("found invalid")
                break
            if "aggressive_player" in line:
                # print("only")
                champion_player = True
            if "=====Round" in line:
                # new round
                # read who is black, who is white, may not use
                i += 1
                player_line = lines[i]
                player_line_list = player_line.strip().split(" ")

                # print(player_line_list)
                start_play = True
                i += 1

                # rest to default
                previous_board_int = 0
                board_int = 0
                black_board_list = []
                white_board_list = []
                winner = None
                continue

            if start_play:
                if "The winner is" in line:
                    # figure out winner
                    winner_str = line[-1]
                    if winner_str == "O":
                        # white wins
                        winner = WHITE
                        # print("white wins")
                    elif winner_str == "X":
                        winner = BLACK
                        # print("black wins")
                    else:
                        raise ValueError
                    # record board list
                    if winner == WHITE:
                        if aggressive_only:
                            win_table.extend(champion_white_board_list)
                            lose_table.extend(champion_black_board_list)
                        else:
                            win_table.extend(white_board_list)
                            lose_table.extend(black_board_list)
                    elif winner == BLACK:
                        if aggressive_only:
                            win_table.extend(champion_black_board_list)
                            lose_table.extend(champion_white_board_list)
                        else:
                            win_table.extend(black_board_list)
                            lose_table.extend(white_board_list)

                    winner = None
                    start_play = False
                    champion_player = False

                if ("Black" in line or "White" in line) and "PASS" not in line:
                    move_list = line.split(" ")[1].split(",")
                    move_i = int(move_list[0])
                    move_j = int(move_list[1])
                    # store state and move
                    if "Black" in line:
                        piece_type = BLACK
                        black_board_list.append([GameBoard.standarize_board(board_int, piece_type), (move_i, move_j)])
                        if champion_player:
                            champion_black_board_list.append(
                                [GameBoard.standarize_board(board_int, piece_type), (move_i, move_j)])
                    else:
                        piece_type = WHITE
                        white_board_list.append([GameBoard.standarize_board(board_int, piece_type), (move_i, move_j)])
                        if champion_player:
                            champion_white_board_list.append(
                                [GameBoard.standarize_board(board_int, piece_type), (move_i, move_j)])

                    temp_board_int, success = GameBoard.place_chess(previous_board_int, board_int, move_i, move_j,
                                                                    piece_type)
                    previous_board_int = board_int
                    d, board_int = GameBoard.remove_died_pieces(temp_board_int, 3 - piece_type)
                    # print("piece{} i: {}, j: {}".format(piece_type, move_i, move_j))
                    # print(GameBoard.visualize_board(board_int))

            # read who wins
            i += 1


def read_stage2_log(path, win_table, lose_table, champion_only=True):
    with open(path, "r") as f:
        lines = f.readlines()
        i = 0
        previous_board_int = 0
        board_int = 0
        black_board_list = []
        white_board_list = []
        champion_black_board_list = []
        champion_white_board_list = []
        winner = None
        start_play = False
        champion_player = False

        while i < len(lines):
            line = lines[i].strip()
            if "ERROR" in line or "not found or invalid format" in line:
                break
            if "Invalid" in line:
                print("found invalid")
                break
            if "championship_player" in line:
                champion_player = True
            if "=====Round" in line:
                # new round
                # read who is black, who is white, may not use
                i += 1
                player_line = lines[i]
                player_line_list = player_line.strip().split(" ")

                # print(player_line_list)
                start_play = True
                i += 1

                # rest to default
                previous_board_int = 0
                board_int = 0
                black_board_list = []
                white_board_list = []
                winner = None
                continue

            if start_play:
                if "The winner is" in line:
                    # figure out winner
                    winner_str = line[-1]
                    if winner_str == "O":
                        # white wins
                        winner = WHITE
                        # print("white wins")
                    elif winner_str == "X":
                        winner = BLACK
                        # print("black wins")
                    else:
                        raise ValueError
                    # record board list
                    if winner == WHITE:
                        if champion_only:
                            win_table.extend(champion_white_board_list)
                            lose_table.extend(champion_black_board_list)
                        else:
                            win_table.extend(white_board_list)
                            lose_table.extend(black_board_list)
                    elif winner == BLACK:
                        if champion_only:
                            win_table.extend(champion_black_board_list)
                            lose_table.extend(champion_white_board_list)
                        else:
                            win_table.extend(black_board_list)
                            lose_table.extend(white_board_list)

                    winner = None
                    start_play = False
                    champion_player = False

                if ("Black" in line or "White" in line) and "PASS" not in line:
                    move_list = line.split(" ")[1].split(",")
                    move_i = int(move_list[0])
                    move_j = int(move_list[1])
                    # store state and move
                    if "Black" in line:
                        piece_type = BLACK
                        black_board_list.append([GameBoard.standarize_board(board_int, piece_type), (move_i, move_j)])
                        if champion_player:
                            champion_black_board_list.append(
                                [GameBoard.standarize_board(board_int, piece_type), (move_i, move_j)])
                    else:
                        piece_type = WHITE
                        white_board_list.append([GameBoard.standarize_board(board_int, piece_type), (move_i, move_j)])
                        if champion_player:
                            champion_white_board_list.append(
                                [GameBoard.standarize_board(board_int, piece_type), (move_i, move_j)])

                    temp_board_int, success = GameBoard.place_chess(previous_board_int, board_int, move_i, move_j,
                                                                    piece_type)
                    previous_board_int = board_int
                    d, board_int = GameBoard.remove_died_pieces(temp_board_int, 3 - piece_type)
                    # print("piece{} i: {}, j: {}".format(piece_type, move_i, move_j))
                    # print(GameBoard.visualize_board(board_int))

            # read who wins
            i += 1


class Learner:
    def __init__(self, initial_value=0.5):
        self.q_values = {}
        self.initial_value = initial_value
        self.champion_win_table = []
        self.champion_lose_table = []
        self.aggressive_win_table = []
        self.aggressive_lose_table = []

    def Q(self, state):
        if state not in self.q_values:
            q_val = np.zeros((5, 5))
            q_val.fill(self.initial_value)
            self.q_values[state] = q_val
        return self.q_values[state]

    def learn_from_champion(self):
        for i in range(1, 200):
            num = str(i)
            try:
                read_stage2_log("s2_submit/cnt{}/history.log".format(num), self.champion_win_table, self.champion_lose_table)
            except:
                print("s2 cnt{} fails".format(num))

        self.learn_from_history(self.champion_win_table, WIN_REWARD)
        self.learn_from_history(self.champion_lose_table, LOSS_REWARD)

    def learn_from_aggressive(self):
        for i in range(1, 100):
            num = str(i)
            try:
                read_stage1_log("s1_submit/cnt{}/history.log".format(num), self.aggressive_win_table, self.aggressive_lose_table)
            except:
                print("s1 cnt{} fails".format(num))

        self.learn_from_history(self.aggressive_win_table, WIN_REWARD)
        # self.learn_from_history(self.aggressive_lose_table, LOSS_REWARD)

    def learn_from_history(self, history, reward, alpha=0.7, gamma=1.0):
        history.reverse()
        max_q_value = -1.0
        for hist in history:
            state, move = hist
            if state == 0:
                max_q_value = -1.0
            self.Q(state)
            q = self.q_values[state]
            if max_q_value < 0:
                q[move[0]][move[1]] = reward
            else:
                q[move[0]][move[1]] = q[move[0]][move[1]] * (1 - alpha) + alpha * (
                        gamma * max_q_value)
            max_q_value = np.max(q)
            print(max_q_value)


if __name__ == "__main__":
    learner = Learner()
    learner.learn_from_champion()
    # learner.learn_from_aggressive()
    # print(learner.q_values)

    FileHandler.write_q_table(learner.q_values)
    print(FileHandler.read_q_table())
    print(len(learner.q_values.keys()))
