import unittest
from unittest.mock import patch

from src.CLI.input_handler.input_handler import InputHandler

class TestInputHandler(unittest.TestCase):

    def test_get_user_input(self):
        prefix = "prefix"
        test_input = "Matthias"

        with patch("builtins.input", return_value=test_input):
            input_handler = InputHandler()
            user_input = input_handler.handle_user_input(prefix)

        assert test_input == user_input