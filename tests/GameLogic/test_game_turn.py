# tests/GameLogic/test_game_turn.py
import unittest
from src.GameLogic.GameTurn import GameTurn
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class test_game_turn(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.guesses = [
            ColorCode.RED,
            ColorCode.BLUE,
            ColorCode.GREEN,
            ColorCode.YELLOW,
        ]
        self.feedback = [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]
        self.game_turn = GameTurn(guesses=self.guesses, feedback=self.feedback)

    def test_initialization(self):
        """Test the initialization of GameTurn."""
        self.assertEqual(self.game_turn.guesses, self.guesses)
        self.assertEqual(self.game_turn.feedback, self.feedback)

    def test_repr(self):
        """Test the string representation of the game turn."""
        expected_repr = f"GameTurn(guesses={self.guesses}, feedback={self.feedback})"
        self.assertEqual(repr(self.game_turn), expected_repr)


if __name__ == "__main__":
    unittest.main()
