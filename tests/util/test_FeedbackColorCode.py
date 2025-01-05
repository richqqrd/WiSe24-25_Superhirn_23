"""Test module for FeedbackColorCode enum."""

import unittest
from src.util.feedback_color_code import FeedbackColorCode


class TestFeedbackColorCode(unittest.TestCase):
    """Test cases for FeedbackColorCode enum."""

    def test_enum_values(self: "TestFeedbackColorCode") -> None:
        """Test that enum values are correctly assigned."""
        self.assertEqual(FeedbackColorCode.WHITE.value, 7)
        self.assertEqual(FeedbackColorCode.BLACK.value, 8)

    def test_get_ansi_code(self: "TestFeedbackColorCode") -> None:
        """Test ANSI color code generation."""
        self.assertEqual(FeedbackColorCode.WHITE.get_ansi_code(), "\033[97m")
        self.assertEqual(FeedbackColorCode.BLACK.get_ansi_code(), "\033[90m")

    def test_str_method(self: "TestFeedbackColorCode") -> None:
        """Test string representation."""
        self.assertEqual(str(FeedbackColorCode.WHITE), "\033[97mWHITE\033[0m")
        self.assertEqual(str(FeedbackColorCode.BLACK), "\033[90mBLACK\033[0m")

    def test_repr_method(self: "TestFeedbackColorCode") -> None:
        """Test repr representation."""
        self.assertEqual(repr(FeedbackColorCode.WHITE), "<FeedbackColorCode.WHITE: 7>")
        self.assertEqual(repr(FeedbackColorCode.BLACK), "<FeedbackColorCode.BLACK: 8>")

    def test_equality(self: "TestFeedbackColorCode") -> None:
        """Test equality comparison."""
        self.assertEqual(FeedbackColorCode.WHITE, FeedbackColorCode.WHITE)
        self.assertEqual(FeedbackColorCode.BLACK, FeedbackColorCode.BLACK)
        self.assertNotEqual(FeedbackColorCode.WHITE, FeedbackColorCode.BLACK)


if __name__ == "__main__":
    unittest.main()
