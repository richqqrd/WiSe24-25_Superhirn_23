"""Test module for ComputerGuesser."""

import unittest
from src.business_logic.guesser.computer_guesser import ComputerGuesser
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class TestComputerGuesser(unittest.TestCase):
    """Test cases for ComputerGuesser class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.positions = 4
        self.colors = 6
        self.guesser = ComputerGuesser(self.positions, self.colors)

    def test_initialization(self):
        """Test initialization of ComputerGuesser."""
        self.assertEqual(self.guesser.positions, self.positions)
        self.assertEqual(self.guesser.colors, self.colors)
        self.assertTrue(self.guesser.first_guess)
        self.assertIsNone(self.guesser.last_guess)
        self.assertGreater(len(self.guesser.possible_codes), 0)

    def test_first_guess(self):
        """Test that first guess follows expected pattern."""
        first_guess = self.guesser.make_guess()
        expected = [ColorCode(1)] * (self.positions // 2) + [ColorCode(2)] * (self.positions - self.positions // 2)
        self.assertEqual(first_guess, expected)
        self.assertFalse(self.guesser.first_guess)

    def test_first_guess_single_color(self):
        """Test first guess with only one available color."""
        guesser = ComputerGuesser(4, 1)
        first_guess = guesser.make_guess()
        expected = [ColorCode(1)] * 4
        self.assertEqual(first_guess, expected)

    def test_calculate_feedback(self):
        """Test feedback calculation."""
        guess = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)]
        code = [ColorCode(1), ColorCode(2), ColorCode(4), ColorCode(3)]

        feedback = self.guesser._calculate_feedback(guess, code)

        black_count = sum(1 for f in feedback if f == FeedbackColorCode.BLACK)
        white_count = sum(1 for f in feedback if f == FeedbackColorCode.WHITE)

        self.assertEqual(black_count, 2)  # Positions 1,2 correct
        self.assertEqual(white_count, 2)  # Colors 3,4 in wrong positions

    def test_would_give_same_feedback(self):
        """Test feedback comparison logic."""
        self.guesser.last_guess = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)]
        test_code = [ColorCode(1), ColorCode(2), ColorCode(4), ColorCode(3)]
        target_feedback = [
            FeedbackColorCode.BLACK,
            FeedbackColorCode.BLACK,
            FeedbackColorCode.WHITE,
            FeedbackColorCode.WHITE
        ]

        result = self.guesser._would_give_same_feedback(test_code, target_feedback)
        self.assertTrue(result)

    def test_process_feedback_reduces_possibilities(self):
        """Test that feedback processing reduces possible codes."""
        first_guess = self.guesser.make_guess()
        initial_count = len(self.guesser.possible_codes)

        feedback = [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]
        self.guesser.process_feedback(feedback)

        self.assertLess(len(self.guesser.possible_codes), initial_count)

    def test_make_guess_after_feedback(self):
        """Test guess generation after feedback."""
        first_guess = self.guesser.make_guess()
        feedback = [FeedbackColorCode.BLACK]
        self.guesser.process_feedback(feedback)

        second_guess = self.guesser.make_guess()
        self.assertNotEqual(first_guess, second_guess)
        self.assertEqual(len(second_guess), self.positions)

    def test_all_possibilities_exhausted(self):
        """Test behavior when no valid codes remain."""
        self.guesser.first_guess = False  # Set first_guess to False
        self.guesser.possible_codes = set()

        with self.assertRaises(ValueError):
            self.guesser.make_guess()

    def test_process_feedback_no_last_guess(self):
        """Test processing feedback without previous guess."""
        self.guesser.last_guess = None
        feedback = [FeedbackColorCode.BLACK]
        self.guesser.process_feedback(feedback)
        # Should not raise any exception


if __name__ == "__main__":
    unittest.main()