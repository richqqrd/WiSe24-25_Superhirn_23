import unittest
from io import StringIO
import sys
from src.cli.game_renderer.game_renderer import GameRenderer
from src.game_logic.game_state import GameState
from src.game_logic.game_turn import GameTurn
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class TestGameRenderer(unittest.TestCase):

    def setUp(self):
        """Set up the test environment by redirecting stdout."""
        self.renderer = GameRenderer()
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore stdout after the test."""
        sys.stdout = sys.__stdout__

    def test_clear_screen(self):
        """Test the clear_screen method to ensure it clears the console."""
        self.renderer.clear_screen()
        output = self.held_output.getvalue().strip()
        self.assertIn(output, ["", "\x1b[2J\x1b[H"])  # Check if the screen is cleared

    def test_colorize(self):
        """Test the colorize method to ensure it correctly applies ANSI codes."""
        pins = [ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE]
        colored_output = self.renderer.colorize(pins)
        expected_output = (
            f"{ColorCode.RED.get_ansi_code()}1\033[0m"
            f"{ColorCode.GREEN.get_ansi_code()}2\033[0m"
            f"{ColorCode.BLUE.get_ansi_code()}4\033[0m"
        )
        self.assertEqual(colored_output, expected_output)

    def test_render_game_state(self):
        """Test the render_game_state method to ensure it
        correctly renders the game state."""
        game_state = GameState([ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE], 12)
        game_state.add_turn(
            GameTurn(
                [ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE],
                [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE],
            )
        )
        game_state.add_turn(
            GameTurn(
                [ColorCode.YELLOW, ColorCode.ORANGE, ColorCode.BROWN],
                [FeedbackColorCode.WHITE, FeedbackColorCode.BLACK],
            )
        )

        self.renderer.render_game_state(game_state)
        output = self.held_output.getvalue().strip()
        self.assertIn("Super Superhirn", output)
        self.assertIn("Round | Feedback | Guess", output)
        self.assertIn(
            f"1     | {FeedbackColorCode.BLACK.get_ansi_code()}8\033[0m"
            f"{FeedbackColorCode.WHITE.get_ansi_code()}7\033[0m | "
            f"{ColorCode.RED.get_ansi_code()}1\033[0m"
            f"{ColorCode.GREEN.get_ansi_code()}2\033[0m"
            f"{ColorCode.BLUE.get_ansi_code()}4\033[0m",
            output,
        )
        self.assertIn(
            f"2     | {FeedbackColorCode.WHITE.get_ansi_code()}7\033[0m"
            f"{FeedbackColorCode.BLACK.get_ansi_code()}8\033[0m | "
            f"{ColorCode.YELLOW.get_ansi_code()}3\033[0m"
            f"{ColorCode.ORANGE.get_ansi_code()}5\033[0m"
            f"{ColorCode.BROWN.get_ansi_code()}6\033[0m",
            output,
        )

    def test_render_message(self):
        """Test the render_message method to ensure it correctly renders a message."""
        self.renderer.render_message("Test Message")
        output = self.held_output.getvalue().strip()
        self.assertIn("Test Message", output)

    def test_render_warning(self):
        """Test the render_warning method to ensure it correctly renders a warning."""
        self.renderer.render_warning("Test Warning")
        output = self.held_output.getvalue().strip()
        self.assertIn("WARNING: Test Warning", output)


if __name__ == "__main__":
    unittest.main()
