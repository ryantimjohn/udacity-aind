"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent
from game_agent import MinimaxPlayer, AlphaBetaPlayer
from sample_players import RandomPlayer

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = AlphaBetaPlayer()
        self.player2 = RandomPlayer()
        self.game = isolation.Board(self.player1, self.player2)

    # def test_example(self):
    #     # TODO: All methods must start with "test_"
    #     self.game.apply_move((2, 3))
    #     self.game.apply_move((0, 5))
    #     print(self.game.to_string())
    #
    #     # get a list of the legal moves available to the active player
    #     print(self.game.get_legal_moves())
    #
    #     # play the remainder of the game automatically -- outcome can be "illegal
    #     # move", "timeout", or "forfeit"
    #     winner, history, outcome = self.game.play()
    #     print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
    #     print(self.game.to_string())
    #     print("Move history:\n{!s}".format(history))
    #     # self.game.play()
    #     # self.assertTrue(False)
    #     # self.fail("Hello, World!")

    def test_alphabeta(self):
        self.game.apply_move((2, 3))
        self.game.apply_move((0, 5))
        print(self.game.to_string())

        # get a list of the legal moves available to the active player
        print(self.game.get_legal_moves())

        # play the remainder of the game automatically -- outcome can be "illegal
        # move", "timeout", or "forfeit"
        winner, history, outcome = self.game.play()
        print("\nWinner: {}\nOutcome: {}".format(winner, outcome))
        print(self.game.to_string())
        print("Move history:\n{!s}".format(history))


if __name__ == '__main__':
    unittest.main()
