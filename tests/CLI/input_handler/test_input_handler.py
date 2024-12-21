# tests/CLI/input_handler/test_input_handler.py
import unittest
from unittest.mock import patch
from src.CLI.input_handler.input_handler import InputHandler


class TestInputHandler(unittest.TestCase):

    def test_handle_user_input(self):
        """
        Test handle_user_input method.
        """
        prefix = "prefix"
        test_input = "Matthias"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_user_input(prefix)

        self.assertEqual(test_input, user_input)

    def test_handle_menu_input(self):
        """
        Test handle_menu_input method.
        """
        test_input = "1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_menu_input()

        self.assertEqual(test_input, user_input)

    def test_handle_role_input(self):
        """
        Test handle_role_input method.
        """
        test_input = "1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_role_input()

        self.assertEqual(test_input, user_input)

    def test_handle_language_input(self):
        """
        Test handle_language_input method.
        """
        test_input = "1"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_language_input()

        self.assertEqual(test_input, user_input)

    def test_handle_code_input(self):
        """
        Test handle_code_input method.
        """
        test_input = "12345"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_code_input()

        self.assertEqual(test_input, user_input)

    def test_handle_guess_input(self):
        """
        Test handle_guess_input method.
        """
        test_input = "12345"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_guess_input()

        self.assertEqual(test_input, user_input)

    def test_handle_feedback_input(self):
        """
        Test handle_feedback_input method.
        """
        test_input = "887"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_feedback_input()

        self.assertEqual(test_input, user_input)


if __name__ == "__main__":
    unittest.main()