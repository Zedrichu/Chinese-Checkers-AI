from game_problem.ChineseCheckers import ChineseCheckers
import unittest


class TestStateHashing(unittest.TestCase):

    def test_equality_two_states(self):
        sut = ChineseCheckers(triangle_size=2)
        state1 = sut.initial_state()
        state2 = sut.initial_state()

        self.assertEqual(state1, state2)

    def test_hashing_two_states(self):
        sut = ChineseCheckers(triangle_size=2)
        state1 = sut.initial_state()
        state2 = sut.initial_state()

        self.assertEqual(hash(state1), hash(state2))

    def test_hashing_two_different_states(self):
        sut = ChineseCheckers(triangle_size=2)
        state1 = sut.initial_state()
        state2 = sut.initial_state()
        state2.board.move((3, 0), (2, 0))

        self.assertNotEqual(hash(state1), hash(state2))