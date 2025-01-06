"""Test module for ColorCode enum."""

import unittest
from src.util.color_code import ColorCode


class TestColorCode(unittest.TestCase):
    """Test cases for ColorCode enum."""

    def test_enum_values(self: "TestColorCode") -> None:
        """Test that enum values are correctly assigned."""
        self.assertEqual(ColorCode.RED.value, 1)
        self.assertEqual(ColorCode.GREEN.value, 2)
        self.assertEqual(ColorCode.YELLOW.value, 3)
        self.assertEqual(ColorCode.BLUE.value, 4)
        self.assertEqual(ColorCode.ORANGE.value, 5)
        self.assertEqual(ColorCode.BROWN.value, 6)
        self.assertEqual(ColorCode.WHITE.value, 7)
        self.assertEqual(ColorCode.BLACK.value, 8)

    def test_get_ansi_code(self: "TestColorCode") -> None:
        """Test ANSI color code generation."""
        self.assertEqual(ColorCode.RED.get_ansi_code(), "\033[31m")
        self.assertEqual(ColorCode.GREEN.get_ansi_code(), "\033[32m")
        self.assertEqual(ColorCode.YELLOW.get_ansi_code(), "\033[33m")
        self.assertEqual(ColorCode.BLUE.get_ansi_code(), "\033[34m")
        self.assertEqual(ColorCode.ORANGE.get_ansi_code(), "\033[38;5;214m")
        self.assertEqual(ColorCode.BROWN.get_ansi_code(), "\033[38;5;94m")
        self.assertEqual(ColorCode.WHITE.get_ansi_code(), "\033[97m")
        self.assertEqual(ColorCode.BLACK.get_ansi_code(), "\033[90m")

    def test_str_method(self: "TestColorCode") -> None:
        """Test string representation."""
        self.assertEqual(str(ColorCode.RED), "\033[31mRED\033[0m")
        self.assertEqual(str(ColorCode.GREEN), "\033[32mGREEN\033[0m")
        self.assertEqual(str(ColorCode.YELLOW), "\033[33mYELLOW\033[0m")
        self.assertEqual(str(ColorCode.BLUE), "\033[34mBLUE\033[0m")
        self.assertEqual(str(ColorCode.ORANGE), "\033[38;5;214mORANGE\033[0m")
        self.assertEqual(str(ColorCode.BROWN), "\033[38;5;94mBROWN\033[0m")
        self.assertEqual(str(ColorCode.WHITE), "\033[97mWHITE\033[0m")
        self.assertEqual(str(ColorCode.BLACK), "\033[90mBLACK\033[0m")

    def test_repr_method(self: "TestColorCode") -> None:
        """Test repr representation."""
        self.assertEqual(repr(ColorCode.RED), "<ColorCode.RED: 1>")
        self.assertEqual(repr(ColorCode.BLACK), "<ColorCode.BLACK: 8>")

    def test_equality(self: "TestColorCode") -> None:
        """Test equality comparison."""
        self.assertEqual(ColorCode.RED, ColorCode.RED)
        self.assertNotEqual(ColorCode.RED, ColorCode.GREEN)
        self.assertNotEqual(ColorCode.RED, ColorCode.BLUE)


if __name__ == "__main__":
    unittest.main()
