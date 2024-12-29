import unittest
from src.GameLogic.Guesser.ComputerGuesser import ComputerGuesser
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class TestComputerGuesser(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a ComputerGuesser instance."""
        self.guesser = ComputerGuesser()

    def test_first_guess(self):
        """Test that the first guess is the predefined pattern"""
        expected = [
            ColorCode(1),
            ColorCode(1),
            ColorCode(2),
            ColorCode(2),
            ColorCode(2),
        ]
        result = self.guesser.make_guess()
        self.assertEqual(result, expected)
        self.assertFalse(self.guesser.first_guess)

    def test_process_feedback_reduces_possible_codes(self):
        """Test that processing feedback reduces the set of possible codes"""
        # Make first guess
        self.guesser.make_guess()
        initial_size = len(self.guesser.possible_codes)

        # Give some feedback (2 black, 1 white)
        feedback = [
            FeedbackColorCode.BLACK,
            FeedbackColorCode.BLACK,
            FeedbackColorCode.WHITE,
        ]
        self.guesser.process_feedback(feedback)

        # Check that possible codes were reduced
        self.assertLess(len(self.guesser.possible_codes), initial_size)

    def test_make_guess_after_feedback(self):
        """Test that subsequent guesses are influenced by feedback"""
        # Make first guess and process feedback
        first_guess = self.guesser.make_guess()
        feedback = [FeedbackColorCode.BLACK]  # Only one correct position
        self.guesser.process_feedback(feedback)

        # Make second guess
        second_guess = self.guesser.make_guess()

        # Verify it's different from first guess
        self.assertNotEqual(first_guess, second_guess)
        self.assertEqual(len(second_guess), 5)

    def test_would_give_same_feedback(self):
        """Test the feedback comparison logic"""
        self.guesser.last_guess = [
            ColorCode(1),
            ColorCode(2),
            ColorCode(3),
            ColorCode(4),
            ColorCode(5),
        ]
        test_code = [
            ColorCode(1),
            ColorCode(2),
            ColorCode(3),
            ColorCode(5),
            ColorCode(4),
        ]
        target_feedback = [
            FeedbackColorCode.BLACK,
            FeedbackColorCode.BLACK,
            FeedbackColorCode.BLACK,
            FeedbackColorCode.WHITE,
            FeedbackColorCode.WHITE,
        ]

        result = self.guesser._would_give_same_feedback(test_code, target_feedback)
        self.assertTrue(result)

    def test_calculate_feedback(self):
        """Test feedback calculation"""
        guess = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4), ColorCode(5)]
        code = [ColorCode(1), ColorCode(2), ColorCode(5), ColorCode(3), ColorCode(4)]

        feedback = self.guesser._calculate_feedback(guess, code)

        # Should have 2 black (positions 1,2) and 3 white (positions 3,4,5)
        black_count = sum(1 for f in feedback if f == FeedbackColorCode.BLACK)
        white_count = sum(1 for f in feedback if f == FeedbackColorCode.WHITE)

        self.assertEqual(black_count, 2)
        self.assertEqual(white_count, 3)

    def test_empty_feedback(self):
        """Test processing empty feedback"""
        self.guesser.make_guess()  # Make first guess
        self.guesser.process_feedback([])

        # Should still be able to make a valid guess
        guess = self.guesser.make_guess()
        self.assertEqual(len(guess), 5)
        self.assertTrue(all(isinstance(color, ColorCode) for color in guess))

    def test_all_possible_codes_exhausted(self):
        """Test behavior when all possible codes are eliminated"""
        self.guesser.possible_codes = set()
        guess = self.guesser.make_guess()

        # Should return the first guess pattern
        expected = [
            ColorCode(1),
            ColorCode(1),
            ColorCode(2),
            ColorCode(2),
            ColorCode(3),
        ]
        self.assertEqual(len(guess), 5)
        self.assertEqual(guess, expected)


if __name__ == "__main__":
    unittest.main()
