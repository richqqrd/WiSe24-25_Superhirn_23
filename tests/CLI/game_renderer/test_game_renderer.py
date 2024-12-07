import unittest
from io import StringIO
import sys
from src.CLI.game_renderer.game_renderer import GameRenderer
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode

class TestGameRenderer(unittest.TestCase):

    def setUp(self):
        self.renderer = GameRenderer()
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_clear_screen(self):
        self.renderer.clear_screen()
        output = self.held_output.getvalue().strip()
        self.assertIn(output, ["", "\x1b[2J\x1b[H"])  # Check if the screen is cleared

    def test_colorize(self):
        pins = [ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE]
        colored_output = self.renderer.colorize(pins)
        expected_output = f"{ColorCode.RED.get_ansi_code()}1\033[0m{ColorCode.GREEN.get_ansi_code()}2\033[0m{ColorCode.BLUE.get_ansi_code()}4\033[0m"
        self.assertEqual(colored_output, expected_output)


    def test_render_game_state(self):
        game_state = {
            1: ([ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE, ColorCode.ORANGE, ColorCode.BROWN], [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE]),
            2: ([ColorCode.YELLOW, ColorCode.ORANGE, ColorCode.BROWN, ColorCode.WHITE, ColorCode.BLACK], [FeedbackColorCode.WHITE, FeedbackColorCode.BLACK])
        }
        self.renderer.render_game_state(game_state)
        output = self.held_output.getvalue().strip()
        self.assertIn("Super Superhirn", output)
        self.assertIn("Round | Feedback | Guess", output)
        self.assertIn("1     | \033[90m8\033[0m\033[97m7\033[0m | \033[31m1\033[0m\033[32m2\033[0m\033[34m4\033[0m\033[38;5;214m5\033[0m\033[38;5;94m6\033[0m", output)
        self.assertIn("2     | \033[97m7\033[0m\033[90m8\033[0m | \033[33m3\033[0m\033[38;5;214m5\033[0m\033[38;5;94m6\033[0m\033[97m7\033[0m\033[90m8\033[0m", output)

    def test_render_message(self):
        self.renderer.render_message("Test Message")
        output = self.held_output.getvalue().strip()
        self.assertIn("Test Message", output)

    def test_render_warning(self):
        self.renderer.render_warning("Test Warning")
        output = self.held_output.getvalue().strip()
        self.assertIn("WARNING: Test Warning", output)

