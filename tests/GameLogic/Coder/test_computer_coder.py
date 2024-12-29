import unittest
from src.GameLogic.Coder.ComputerCoder import ComputerCoder
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class test_computer_coder(unittest.TestCase):
    """
    Unit tests for the ComputerCoder class.
    """

    def setUp(self):
        """
        Set up the test environment by initializing a ComputerCoder instance.
        """
        self.coder = ComputerCoder()

    def test_generate_code(self):
        """
        Test the generate_code method to ensure it generates a code of length 5
        with valid ColorCode instances.
        """
        code = self.coder.generate_code()
        self.assertEqual(len(code), 5)
        for color in code:
            self.assertIsInstance(color, ColorCode)
            self.assertTrue(1 <= color.value <= 8)

    def test_give_feedback_all_correct(self):
        """
        Test the give_feedback method to ensure it returns all black feedback
        when the guess is completely correct.
        """
        self.coder.secret_code = [
            ColorCode(1),
            ColorCode(2),
            ColorCode(3),
            ColorCode(4),
            ColorCode(5),
        ]
        guess = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4), ColorCode(5)]

        feedback = self.coder.give_feedback(guess)
        self.assertEqual(len(feedback), 5)
        self.assertTrue(all(f == FeedbackColorCode.BLACK for f in feedback))

    def test_give_feedback_all_wrong(self):
        """
        Test the give_feedback method to ensure it returns no feedback
        when the guess is completely incorrect.
        """
        self.coder.secret_code = [
            ColorCode(1),
            ColorCode(2),
            ColorCode(3),
            ColorCode(4),
            ColorCode(5),
        ]
        guess = [ColorCode(6), ColorCode(7), ColorCode(8), ColorCode(6), ColorCode(7)]

        feedback = self.coder.give_feedback(guess)
        self.assertEqual(len(feedback), 0)

    def test_give_feedback_mixed(self):
        """
        Test the give_feedback method to ensure it returns a mix of
        black and white feedback
        when the guess is partially correct.
        """
        self.coder.secret_code = [
            ColorCode(1),
            ColorCode(2),
            ColorCode(3),
            ColorCode(4),
            ColorCode(5),
        ]
        guess = [ColorCode(1), ColorCode(3), ColorCode(2), ColorCode(6), ColorCode(4)]

        feedback = self.coder.give_feedback(guess)

        # Count black (correct position) and white (wrong position) pins
        black_count = sum(1 for f in feedback if f == FeedbackColorCode.BLACK)
        white_count = sum(1 for f in feedback if f == FeedbackColorCode.WHITE)

        self.assertEqual(black_count, 1)  # 1 and 4 are in correct positions
        self.assertEqual(white_count, 3)  # 2 and 3 are in wrong positions


if __name__ == "__main__":
    unittest.main()
