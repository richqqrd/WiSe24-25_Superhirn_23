"""Test module for PlayerGuesser."""

import unittest
from src.business_logic.guesser.player_guesser import PlayerGuesser
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class TestPlayerGuesser(unittest.TestCase):
    """Test suite for the PlayerGuesser class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.guesser = PlayerGuesser()
        self.test_guess = [ColorCode(1), ColorCode(2), ColorCode(3)]
        self.test_feedback = [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]

    def test_initialization(self):
        """Test initialization of PlayerGuesser."""
        self.assertIsInstance(self.guesser, PlayerGuesser)
        self.assertEqual(self.guesser.current_guess, [])

    def test_make_guess_empty(self):
        """Test make_guess with no guess set."""
        result = self.guesser.make_guess()
        self.assertEqual(result, [])

    def test_set_and_make_guess(self):
        """Test setting and retrieving a guess."""
        self.guesser.set_guess(self.test_guess)
        result = self.guesser.make_guess()
        self.assertEqual(result, self.test_guess)

    def test_set_guess_multiple_times(self):
        """Test setting multiple guesses."""
        first_guess = [ColorCode(1), ColorCode(2)]
        second_guess = [ColorCode(3), ColorCode(4)]

        self.guesser.set_guess(first_guess)
        self.assertEqual(self.guesser.make_guess(), first_guess)

        self.guesser.set_guess(second_guess)
        self.assertEqual(self.guesser.make_guess(), second_guess)

    def test_process_feedback(self):
        """Test processing feedback."""
        # Should not change state as it's not used in player implementation
        initial_guess = self.guesser.current_guess.copy()
        self.guesser.process_feedback(self.test_feedback)
        self.assertEqual(self.guesser.current_guess, initial_guess)

    def test_set_guess_empty_list(self):
        """Test setting an empty guess."""
        self.guesser.set_guess([])
        self.assertEqual(self.guesser.make_guess(), [])

    def test_set_guess_none(self):
        """Test setting guess to None."""
        self.guesser.set_guess(None)
        self.assertEqual(self.guesser.make_guess(), [])


if __name__ == "__main__":
    unittest.main()