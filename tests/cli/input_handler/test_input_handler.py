# tests/cli/input_handler/test_input_handler.py
import unittest
from unittest.mock import patch
from src.cli.input_handler.input_handler import InputHandler


class TestInputHandler(unittest.TestCase):

    def test_handle_user_input(self):
        """Test handle_user_input method."""
        prefix = "prefix"
        test_input = "Matthias"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_user_input(prefix)

        self.assertEqual(test_input, user_input)

    def test_handle_menu_input(self):
        """Test handle_menu_input method."""
        test_input = "1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_menu_input()

        self.assertEqual(test_input, user_input)

    def test_handle_game_mode_input(self):
        """Test handle_game_mode_input method."""
        test_input = "1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_game_mode_input()

        self.assertEqual(test_input, user_input)

    def test_handle_language_input_valid(self):
        """Test handle_language_input method with valid input."""
        test_input = "1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_language_input("en")

        self.assertEqual(user_input, "en")

    def test_handle_language_input_invalid_index(self):
        """Test handle_language_input method with invalid index input."""
        test_input = "99"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_language_input("en")

        self.assertEqual(user_input, "en")

    def test_handle_language_input_invalid_value(self):
        """Test handle_language_input method with invalid value input."""
        test_input = "invalid"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_language_input("en")

        self.assertEqual(user_input, "en")

    def test_handle_code_input(self):
        """Test handle_code_input method."""
        test_input = "12345"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_code_input(5)

        self.assertEqual(test_input, user_input)

    def test_handle_guess_input(self):
        """Test handle_guess_input method."""
        test_input = "12345"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_guess_input(5)

        self.assertEqual(test_input, user_input)

    def test_handle_feedback_input(self):
        """Test handle_feedback_input method."""
        test_input = "887"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_feedback_input(3)

        self.assertEqual(test_input, user_input)

    def test_handle_ip_input(self):
        """Test handle_ip_input method."""
        test_input = "192.168.0.1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_ip_input()

        self.assertEqual(test_input, user_input)

    def test_handle_port_input(self):
        """Test handle_port_input method."""
        test_input = "8080"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_port_input()

        self.assertEqual(test_input, user_input)

    def test_handle_player_name_input(self):
        """Test handle_player_name_input method."""
        test_input = "Player1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_player_name_input()

        self.assertEqual(test_input, user_input)

    def test_handle_positions_input(self):
        """Test handle_positions_input method."""
        test_input = "4"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_positions_input()

        self.assertEqual(test_input, user_input)

    def test_handle_colors_input(self):
        """Test handle_colors_input method."""
        test_input = "6"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_colors_input()

        self.assertEqual(test_input, user_input)

    def test_handle_max_attempts_input(self):
        """Test handle_max_attempts_input method."""
        test_input = "10"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_max_attempts_input()

        self.assertEqual(test_input, user_input)

    def test_handle_save_warning_input_yes(self):
        """Test handle_save_warning_input method for 'yes'."""
        test_input = "1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_save_warning_input()

        self.assertTrue(user_input)

    def test_handle_save_warning_input_no(self):
        """Test handle_save_warning_input method for 'no'."""
        test_input = "2"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_save_warning_input()

        self.assertFalse(user_input)

    def test_set_language(self):
        """Test set_language method."""
        input_handler = InputHandler()
        input_handler.set_language("de")
        self.assertEqual(input_handler.language, "de")

        input_handler.set_language("invalid")
        self.assertEqual(input_handler.language, "de")  # Should remain unchanged

    def test_handle_user_input_empty(self):
        """Test handle_user_input method with empty input."""
        prefix = "prefix"
        test_input = ""

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_user_input(prefix)

        self.assertEqual(test_input, user_input)

    def test_handle_user_input_whitespace(self):
        """Test handle_user_input method with whitespace input."""
        prefix = "prefix"
        test_input = "   "

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_user_input(prefix)

        self.assertEqual(test_input, user_input)

    def test_handle_code_input_invalid_characters(self):
        """Test handle_code_input method with invalid characters."""
        test_input = "abcde"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_code_input(5)

        self.assertEqual(test_input, user_input)

    def test_handle_code_input_special_characters(self):
        """Test handle_code_input method with special characters."""
        test_input = "!@#$%"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_code_input(5)

        self.assertEqual(test_input, user_input)

    def test_handle_code_input_long_input(self):
        """Test handle_code_input method with long input."""
        test_input = "1234567890"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_code_input(5)

        self.assertEqual(test_input, user_input)

    def test_handle_language_input_empty(self):
        """Test handle_language_input method with empty input."""
        test_input = ""

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_language_input("en")

        self.assertEqual(user_input, "en")

    def test_handle_language_input_whitespace(self):
        """Test handle_language_input method with whitespace input."""
        test_input = "   "

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_language_input("en")

        self.assertEqual(user_input, "en")

if __name__ == "__main__":
    unittest.main()