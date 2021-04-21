from myplayer_play.Greedy.my_player3 import GreedyPlayer
from myplayer_play.random_player import RandomPlayer
import myplayer_play.go as go
import myplayer_play.GameBoard as GameBoard
import numpy as np


def run(my_player, other_player, params, f):
    num = 5
    verbose = False
    p1_status = go.battle(my_player, other_player, num, learn=True, show_result=False, verbose=verbose)
    p2_status = go.battle(other_player, my_player, num, learn=True, show_result=False, verbose=verbose)
    # print(p1_status)  # draw, win, lose
    # print(p2_status)  # draw, win, lose
    win_rate = (p1_status[1], p2_status[2])
    print(win_rate)
    s = "["
    s += ",".join(str(p) for p in params)
    s += "], (" + str(win_rate[0]) + ", " + str(win_rate[1]) + ")\n"
    f.write(s)

if __name__ == "__main__":
    f = open("tune_result.txt", "a+")
    my_player = GreedyPlayer()
    other_player = GreedyPlayer()
    for win_s in np.arange(0.0, 5, 1):
        for kill_s in np.arange(0.0, 5, 1):
            for kill_s2 in np.arange(0.0, 5, 1):
                for be_killed_s in np.arange(0.0, 5, 1):
                    for liberty_s in np.arange(0.0, 5, 1):
                        for connection_score in np.arange(0.0, 5, 1):
                            for edge_s in np.arange(0.0, 5, 1):
                                params = [win_s, kill_s, kill_s2, be_killed_s, liberty_s, connection_score, edge_s]
                                my_player.params = params
                                run(my_player, other_player, params, f)
    f.close()
