"""Test module for ComputerCoder."""

import unittest
from src.business_logic.coder.computer_coder import ComputerCoder
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class TestComputerCoder(unittest.TestCase):
    """Test cases for ComputerCoder class."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.positions = 4
        self.colors = 6
        self.coder = ComputerCoder(self.positions, self.colors)

    def test_initialization(self):
        """Test initialization of ComputerCoder."""
        self.assertEqual(self.coder.positions, self.positions)
        self.assertEqual(self.coder.colors, self.colors)
        self.assertEqual(self.coder.secret_code, [])

    def test_generate_code(self):
        """Test code generation."""
        code = self.coder.generate_code()

        # Test length
        self.assertEqual(len(code), self.positions)

        # Test valid colors
        for color in code:
            self.assertIsInstance(color, ColorCode)
            self.assertTrue(1 <= color.value <= self.colors)

    def test_give_feedback_all_correct(self):
        """Test feedback for completely correct guess."""
        secret = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)]
        self.coder.secret_code = secret

        feedback = self.coder.give_feedback(secret)

        self.assertEqual(len(feedback), self.positions)
        self.assertTrue(all(f == FeedbackColorCode.BLACK for f in feedback))

    def test_give_feedback_all_wrong(self):
        """Test feedback for completely wrong guess."""
        self.coder.secret_code = [ColorCode(1)] * self.positions
        guess = [ColorCode(2)] * self.positions

        feedback = self.coder.give_feedback(guess)

        self.assertEqual(len(feedback), 0)

    def test_give_feedback_mixed(self):
        """Test feedback for partially correct guess."""
        self.coder.secret_code = [
            ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)
        ]
        guess = [ColorCode(1), ColorCode(3), ColorCode(2), ColorCode(5)]

        feedback = self.coder.give_feedback(guess)

        black_count = sum(1 for f in feedback if f == FeedbackColorCode.BLACK)
        white_count = sum(1 for f in feedback if f == FeedbackColorCode.WHITE)

        self.assertEqual(black_count, 1)  # Position 1 correct
        self.assertEqual(white_count, 2)  # Colors 2,3 in wrong positions

    def test_give_feedback_wrong_length(self):
        """Test feedback for guess with wrong length."""
        self.coder.secret_code = [ColorCode(1)] * self.positions
        guess = [ColorCode(1)]  # Too short

        feedback = self.coder.give_feedback(guess)
        self.assertEqual(len(feedback), 0)

    def test_secret_code_property(self):
        """Test secret code getter/setter."""
        test_code = [ColorCode(1), ColorCode(2), ColorCode(3), ColorCode(4)]
        self.coder.secret_code = test_code
        self.assertEqual(self.coder.secret_code, test_code)

    def test_multiple_code_generation(self):
        """Test multiple code generations."""
        codes = set()
        for _ in range(10):
            code = tuple(c.value for c in self.coder.generate_code())
            codes.add(code)
        # Test that we got some variety in the generated codes
        self.assertGreater(len(codes), 1)


if __name__ == "__main__":
    unittest.main()