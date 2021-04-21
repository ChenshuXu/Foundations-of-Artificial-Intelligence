from unittest import TestCase
import myplayer_play.QLearner.ExtractResults as ExtractResults


class Test(TestCase):
    def test_read_log(self):
        ExtractResults.read_stage2_log(path="history.log")
