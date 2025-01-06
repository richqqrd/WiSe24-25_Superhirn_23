"""Test cases for the GameRenderer class."""

import unittest
from io import StringIO
import sys

from src.business_logic.guesser.computer_guesser import ComputerGuesser
from src.cli.game_renderer.game_renderer import GameRenderer
from src.business_logic.game_state import GameState
from src.business_logic.game_turn import GameTurn
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.util.translations import translations


class TestGameRenderer(unittest.TestCase):
    """Test cases for the GameRenderer class."""

    def setUp(self: "TestGameRenderer") -> None:
        """Set up the test environment by redirecting stdout."""
        self.renderer = GameRenderer()
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self: "TestGameRenderer") -> None:
        """Restore stdout after the test."""
        sys.stdout = sys.__stdout__

    def test_clear_screen(self: "TestGameRenderer") -> None:
        """Test the clear_screen method to ensure it clears the console."""
        self.renderer.clear_screen()
        output = self.held_output.getvalue().strip()
        self.assertIn(output, ["", "\x1b[2J\x1b[H"])  # Check if the screen is cleared

    def test_colorize(self: "TestGameRenderer") -> None:
        """Test the colorize method to ensure it correctly applies ANSI codes."""
        pins = [ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE]
        colored_output = self.renderer.colorize(pins)
        expected_output = (
            f"     {ColorCode.RED.get_ansi_code()}1\033[0m "
            f"{ColorCode.GREEN.get_ansi_code()}2\033[0m "
            f"{ColorCode.BLUE.get_ansi_code()}4\033[0m     "
        )
        self.assertEqual(colored_output, expected_output)

    def test_colorize_empty_pins(self: "TestGameRenderer") -> None:
        """Test the colorize method with an empty list of pins."""
        colored_output = self.renderer.colorize([])
        expected_output = " " * 15  # Default width is 15
        self.assertEqual(colored_output, expected_output)

    def test_render_game_state(self: "TestGameRenderer") -> None:
        """Test the render_game_state method."""
        game_state = GameState(
            secret_code=[ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE,
                         ColorCode.YELLOW],
            positions=4,
            colors=6,
            max_rounds=12,
            player_name="Player"
        )
        game_state.add_turn(
            GameTurn(
                [ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE, ColorCode.YELLOW],
                [FeedbackColorCode.BLACK, FeedbackColorCode.WHITE],
            )
        )
        game_state.add_turn(
            GameTurn(
                [ColorCode.YELLOW, ColorCode.ORANGE, ColorCode.BROWN, ColorCode.GREEN],
                [FeedbackColorCode.WHITE, FeedbackColorCode.BLACK],
            )
        )

        self.renderer.render_game_state(game_state)
        output = self.held_output.getvalue().strip()
        self.assertIn("Super Mastermind", output)
        self.assertIn(" Round   |    Feedback     |      Guess     ", output)
        self.assertIn(
            f"   1     |       {FeedbackColorCode.BLACK.get_ansi_code()}8\033[0m "
            f"{FeedbackColorCode.WHITE.get_ansi_code()}7\033[0m       |     "
            f"{ColorCode.RED.get_ansi_code()}1\033[0m "
            f"{ColorCode.GREEN.get_ansi_code()}2\033[0m "
            f"{ColorCode.BLUE.get_ansi_code()}4\033[0m "
            f"{ColorCode.YELLOW.get_ansi_code()}3\033[0m    ",
            output,
        )
        self.assertIn(
            f"   2     |       {FeedbackColorCode.WHITE.get_ansi_code()}7\033[0m "
            f"{FeedbackColorCode.BLACK.get_ansi_code()}8\033[0m       |     "
            f"{ColorCode.YELLOW.get_ansi_code()}3\033[0m "
            f"{ColorCode.ORANGE.get_ansi_code()}5\033[0m "
            f"{ColorCode.BROWN.get_ansi_code()}6\033[0m "
            f"{ColorCode.GREEN.get_ansi_code()}2\033[0m    ",
            output,
        )

    def test_render_game_state_with_secret_code(self: "TestGameRenderer") -> None:
        """Test the render_game_state method with a secret code."""
        game_state = GameState(
            secret_code=[ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE,
                         ColorCode.YELLOW],
            positions=4,
            colors=6,
            max_rounds=12,
            player_name="Player",
            current_guesser=ComputerGuesser(4, 6)
        )

        self.renderer.render_game_state(game_state)
        output = self.held_output.getvalue().strip()
        secret_code_str = self.renderer.colorize(game_state.secret_code)
        self.assertIn(f"{translations[self.renderer.language]['secret_code']}: "
                      f"{secret_code_str}", output)

    def test_render_game_state_none(self: "TestGameRenderer") -> None:
        """Test the render_game_state method with a None game state."""
        self.renderer.render_game_state(None)
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "")  # No output should be produced

    def test_render_message(self: "TestGameRenderer") -> None:
        """Test the render_message method to ensure it correctly renders a message."""
        self.renderer.render_message("Test Message")
        output = self.held_output.getvalue().strip()
        self.assertIn("Test Message", output)

    def test_render_warning(self: "TestGameRenderer") -> None:
        """Test the render_warning method to ensure it correctly renders a warning."""
        self.renderer.render_warning("Test Warning")
        output = self.held_output.getvalue().strip()
        self.assertIn("WARNING:          Test Warning         ", output)

    def test_set_language(self: "TestGameRenderer") -> None:
        """Test the set_language method to ensure it sets the language correctly."""
        renderer = GameRenderer()

        # Test setting a valid language
        renderer.set_language("de")
        self.assertEqual(renderer.language, "de")

        # Test setting an invalid language
        renderer.set_language("invalid_language")
        self.assertEqual(renderer.language, "de")  # Language should remain unchanged

    def test_set_language_invalid(self: "TestGameRenderer") -> None:
        """Test setting an invalid language code."""
        self.renderer.set_language("invalid")
        self.assertEqual(self.renderer.language, "en")  # Should remain unchanged

    def test_render_message_long(self: "TestGameRenderer") -> None:
        """Test rendering a long message."""
        long_message = ("This is a very long message that should be tested"
                        "to see how it is handled by the renderer.")
        self.renderer.render_message(long_message)
        output = self.held_output.getvalue().strip()
        # Check if part of the long message is in the output
        self.assertIn(long_message[:40], output)

    def test_render_game_state_special_characters(self: "TestGameRenderer") -> None:
        """Test rendering a game state with special characters in the player name."""
        game_state = GameState(
            secret_code=[ColorCode.RED, ColorCode.GREEN, ColorCode.BLUE,
                         ColorCode.YELLOW],
            positions=4,
            colors=6,
            max_rounds=12,
            player_name="Player!@#"
        )
        self.renderer.render_game_state(game_state)
        output = self.held_output.getvalue().strip()
        self.assertIn("Player!@#", output)


if __name__ == "__main__":
    unittest.main()
