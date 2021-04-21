from unittest import TestCase
import myplayer_play.FileHandler as FileHandler

BLACK = 1
WHITE = 2

class Test(TestCase):
    def test_write_qtable(self):
        temp = {6661:456456}
        FileHandler.write_q_table(temp)

    def test_read_qtable(self):
        temp = FileHandler.read_q_table()
        print(temp)

    def test_read_qtable2(self):
        temp = FileHandler.read_q_table(path="QTable_from_run.pkl")
        print(temp)
