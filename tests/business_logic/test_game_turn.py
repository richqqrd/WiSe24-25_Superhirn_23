"""Tests/business_logic/test_game_turn.py."""
import unittest
from src.business_logic.game_turn import GameTurn
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class test_game_turn(unittest.TestCase):
    """Test the GameTurn class."""

    def setUp(self: "test_game_turn") -> None:
        """Set up the test environment."""
        self.guesses = [
            ColorCode.RED,
            ColorCode.BLUE,
            ColorCode.GREEN,
            ColorCode.YELLOW,
        ]
        self.feedback = [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]
        self.game_turn = GameTurn(guesses=self.guesses, feedback=self.feedback)

    def test_initialization(self: "test_game_turn") -> None:
        """Test the initialization of GameTurn."""
        self.assertEqual(self.game_turn.guesses, self.guesses)
        self.assertEqual(self.game_turn.feedback, self.feedback)

    def test_repr(self: "test_game_turn") -> None:
        """Test the string representation of the game turn."""
        expected_repr = f"GameTurn(guesses={self.guesses}, feedback={self.feedback})"
        self.assertEqual(repr(self.game_turn), expected_repr)


if __name__ == "__main__":
    unittest.main()
