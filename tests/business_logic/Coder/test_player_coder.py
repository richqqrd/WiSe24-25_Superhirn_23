"""Test module for PlayerCoder class."""

import unittest
from src.business_logic.coder.player_coder import PlayerCoder
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class TestPlayerCoder(unittest.TestCase):
    """Test cases for the PlayerCoder class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.coder = PlayerCoder()
        self.test_code = [ColorCode.RED, ColorCode.BLUE, ColorCode.GREEN]
        self.test_guess = [ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE]

    def test_initialization(self):
        """Test initialization of PlayerCoder."""
        self.assertIsInstance(self.coder, PlayerCoder)
        self.assertEqual(self.coder.code, [])

    def test_generate_code_empty(self):
        """Test generate_code with empty code list."""
        with self.assertRaises(ValueError):
            self.coder.generate_code()

    def test_generate_code_with_code(self):
        """Test generate_code with preset code."""
        self.coder.code = self.test_code
        result = self.coder.generate_code()
        self.assertEqual(result, self.test_code)

    def test_give_feedback_empty(self):
        """Test give_feedback with no feedback set."""
        result = self.coder.give_feedback()
        self.assertIsNone(result)

    def test_set_and_give_feedback(self):
        """Test setting and retrieving feedback."""
        test_feedback = [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]
        self.coder.current_feedback = test_feedback
        result = self.coder.give_feedback()
        self.assertIsNone(result)  # Erwarte None als Rückgabewert

    def test_set_and_get_code(self):
        """Test setting and getting code through direct attribute access."""
        self.coder.code = self.test_code
        self.assertEqual(self.coder.code, self.test_code)

    def test_code_initialization(self):
        """Test code initialization."""
        self.assertEqual(self.coder.code, [])

    def test_code_none(self):
        """Test setting code to None."""
        self.coder.code = None
        self.assertIsNone(self.coder.code)


if __name__ == "__main__":
    unittest.main()
