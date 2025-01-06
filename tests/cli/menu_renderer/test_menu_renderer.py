"""Test cases for the MenuRenderer class."""
import unittest
from io import StringIO
import sys

from src.cli.menu_renderer.menu_renderer import MenuRenderer
from src.util.color_code import ColorCode


class TestMenuRenderer(unittest.TestCase):
    """Test cases for the MenuRenderer class."""

    def setUp(self: "TestMenuRenderer") -> None:
        """Set up the test environment by redirecting stdout."""
        self.renderer = MenuRenderer()
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self: "TestMenuRenderer") -> None:
        """Reset the test environment by restoring stdout."""
        sys.stdout = sys.__stdout__

    def test_display_main_menu(self: "TestMenuRenderer") -> None:
        """Test the display_main_menu method."""
        self.renderer.display_main_menu(["resume_game"])
        output = self.held_output.getvalue().strip()
        self.assertIn("Main Menu", output)
        self.assertIn("1. Start Game", output)
        self.assertIn("2. Change Language", output)
        self.assertIn("3. Resume Interrupted Game", output)
        self.assertIn("4. End Game", output)

    def test_display_ingame_menu(self: "TestMenuRenderer") -> None:
        """Test the display_ingame_menu method."""
        self.renderer.display_ingame_menu(["save_game"])
        output = self.held_output.getvalue().strip()
        self.assertIn("Menu", output)
        self.assertIn("1. Save Game", output)
        self.assertIn("2. Change Language", output)
        self.assertIn("3. Back to Main Menu", output)
        self.assertIn("4. End Game", output)

    def test_display_ingame_menu_with_resume_game(self: "TestMenuRenderer") -> None:
        """Test the display_ingame_menu method."""
        # Simulate saving a game
        self.renderer.display_save_game()

        # Now display the in-game menu with 'resume_game' available
        self.renderer.display_ingame_menu(["save_game", "resume_game"])
        output = self.held_output.getvalue().strip()
        self.assertIn("Menu", output)
        self.assertIn("1. Save Game", output)
        self.assertIn("2. Change Language", output)
        self.assertIn("3. Resume Interrupted Game", output)
        self.assertIn("4. Back to Main Menu", output)
        self.assertIn("5. End Game", output)

    def test_display_ingame_menu_without_resume_game(self: "TestMenuRenderer") -> None:
        """Test the display_ingame_menu method."""
        self.renderer.display_ingame_menu([])
        output = self.held_output.getvalue().strip()
        self.assertIn("Menu", output)
        self.assertIn("1. Change Language", output)
        self.assertIn("2. Back to Main Menu", output)
        self.assertIn("3. End Game", output)

    def test_display_game_mode_menu(self: "TestMenuRenderer") -> None:
        """Test the display_game_mode_menu method."""
        self.renderer.display_game_mode_menu()
        output = self.held_output.getvalue().strip()
        self.assertIn("Select game mode:", output)
        self.assertIn("1. Start Offline Game as guesser", output)
        self.assertIn("2. Start Offline Game as coder", output)
        self.assertIn("3. Start Online Game as guesser", output)
        self.assertIn("4. Let the computer guess (online)", output)
        self.assertIn("5. Back to Main Menu", output)

    def test_display_languages(self: "TestMenuRenderer") -> None:
        """Test the display_languages method."""
        self.renderer.display_languages()
        output = self.held_output.getvalue().strip()
        self.assertIn("Select a language:", output)
        self.assertIn("1. English", output)
        self.assertIn("2. German", output)

    def test_display_end_game(self: "TestMenuRenderer") -> None:
        """Test the display_end_game method."""
        self.renderer.display_end_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game ended.", output)

    def test_display_save_game(self: "TestMenuRenderer") -> None:
        """Test the display_save_game method."""
        self.renderer.display_save_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game saved.", output)

    def test_display_load_game(self: "TestMenuRenderer") -> None:
        """Test the display_load_game method."""
        self.renderer.display_load_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("loads resumed game", output)

    def test_display_start_game(self: "TestMenuRenderer") -> None:
        """Test the display_start_game method."""
        self.renderer.display_start_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game started.", output)

    def test_display_code_input(self: "TestMenuRenderer") -> None:
        """Test the display_code_input method."""
        self.renderer.display_code_input(6)
        output = self.held_output.getvalue().strip()
        self.assertIn("Available colors and their codes:", output)
        for color in list(ColorCode)[:6]:
            self.assertIn(f"{color.value}: {color}", output)

    def test_display_guess_input(self: "TestMenuRenderer") -> None:
        """Test the display_guess_input method."""
        self.renderer.display_guess_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Available colors and their codes:", output)
        for color in ColorCode:
            self.assertIn(f"{color.value} : {color}", output)

    def test_display_feedback_input(self: "TestMenuRenderer") -> None:
        """Test the display_feedback_input method."""
        self.renderer.display_feedback_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Give feedback for the guess:", output)
        self.assertIn("8: Black (correct color in correct position)", output)
        self.assertIn("7: White (correct color in wrong position)", output)
        self.assertIn("Enter feedback (e.g. 887 for two black, one white):", output)

    def test_display_server_connection(self: "TestMenuRenderer") -> None:
        """Test the display_server_connection method."""
        self.renderer.display_server_connection()
        output = self.held_output.getvalue().strip()
        self.assertIn("Enter server IP address:", output)
        self.assertIn("Enter server port:", output)

    def test_display_cheating_warning(self: "TestMenuRenderer") -> None:
        """Test the display_cheating_warning method."""
        self.renderer.display_cheating_warning()
        output = self.held_output.getvalue().strip()
        self.assertIn("CHEATING DETECTED!", output)

    def test_display_player_name_input(self: "TestMenuRenderer") -> None:
        """Test the display_player_name_input method."""
        self.renderer.display_player_name_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Pick a player name", output)

    def test_display_positions_input(self: "TestMenuRenderer") -> None:
        """Test the display_positions_input method."""
        self.renderer.display_positions_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Pick with how many positions you want to play", output)

    def test_display_colors_input(self: "TestMenuRenderer") -> None:
        """Test the display_colors_input method."""
        self.renderer.display_colors_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Pick how many colors you want to play with", output)

    def test_display_max_attempts_input(self: "TestMenuRenderer") -> None:
        """Test the display_max_attempts_input method."""
        self.renderer.display_max_attempts_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Pick the maximum number of attempts", output)

    def test_display_save_warning(self: "TestMenuRenderer") -> None:
        """Test the display_save_warning method."""
        self.renderer.display_save_warning()
        output = self.held_output.getvalue().strip()
        self.assertIn("Warning: A saved game already exists and will be overwritten."
                      " Continue?", output)

    def test_display_color_selection(self: "TestMenuRenderer") -> None:
        """Test the display_color_selection method."""
        self.renderer.display_color_selection()
        output = self.held_output.getvalue().strip()
        self.assertIn("Available colors and their codes:", output)
        for color in ColorCode:
            self.assertIn(f"{color.value} : {color}", output)
        self.assertIn("Enter number of colors:", output)

    def test_display_feedback_instructions(self: "TestMenuRenderer") -> None:
        """Test the display_feedback_instructions method."""
        self.renderer.display_feedback_instructions()
        output = self.held_output.getvalue().strip()
        self.assertIn("8: Black (correct color in correct position)", output)
        self.assertIn("7: White (correct color in wrong position)", output)
        self.assertIn("Enter feedback (e.g. 887 for two black, one white):", output)

    def test_display_invalid_configuration(self: "TestMenuRenderer") -> None:
        """Test the invalid configuration message."""
        self.renderer.display_invalid_configuration()
        output = self.held_output.getvalue().strip()
        self.assertIn("Invalid configuration.", output)

    def test_display_game_won(self: "TestMenuRenderer") -> None:
        """Test the game won message."""
        self.renderer.display_game_won()
        output = self.held_output.getvalue().strip()
        self.assertIn("Congratulations! You've won the game!", output)

    def test_display_game_lost(self: "TestMenuRenderer") -> None:
        """Test the game lost message."""
        self.renderer.display_game_lost()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game Over!\nReturn to main menu in 3 seconds...", output)

    def test_set_language_valid(self: "TestMenuRenderer") -> None:
        """Test the set_language method with a valid language code."""
        self.renderer.set_language("de")
        self.assertEqual(self.renderer.language, "de")

    def test_set_language_invalid(self: "TestMenuRenderer") -> None:
        """Test the set_language method with an invalid language code."""
        self.renderer.set_language("invalid")
        self.assertEqual(self.renderer.language, "en")

    def test_display_ingame_menu_without_save_game(self: "TestMenuRenderer") -> None:
        """Test the display_ingame_menu method without the 'save_game' action."""
        self.renderer.display_ingame_menu([])
        output = self.held_output.getvalue().strip()
        self.assertIn("Menu", output)
        self.assertIn("1. Change Language", output)
        self.assertIn("2. Back to Main Menu", output)
        self.assertIn("3. End Game", output)

    def test_set_language_empty(self: "TestMenuRenderer") -> None:
        """Test the set_language method with an empty language code."""
        self.renderer.set_language("")
        self.assertEqual(self.renderer.language, "en")

    def test_set_language_unsupported(self: "TestMenuRenderer") -> None:
        """Test the set_language method with an unsupported language code."""
        self.renderer.set_language("unsupported")
        self.assertEqual(self.renderer.language, "en")

    def test_display_ingame_menu_empty_actions(self: "TestMenuRenderer") -> None:
        """Test the display_ingame_menu method."""
        # with an empty list of available actions.

        self.renderer.display_ingame_menu([])
        output = self.held_output.getvalue().strip()
        self.assertIn("Menu", output)
        self.assertIn("1. Change Language", output)
        self.assertIn("2. Back to Main Menu", output)
        self.assertIn("3. End Game", output)

    def test_display_ingame_menu_partial_actions(self: "TestMenuRenderer") -> None:
        """Test the display_ingame_menu method."""
        # with a partial list of available actions.

        self.renderer.display_ingame_menu(["resume_game"])
        output = self.held_output.getvalue().strip()
        self.assertIn("Menu", output)
        self.assertIn("1. Change Language", output)
        self.assertIn("2. Back to Main Menu", output)
        self.assertIn("3. End Game", output)

    def test_display_code_input_zero_colors(self: "TestMenuRenderer") -> None:
        """Test the display_code_input method with zero available colors."""
        self.renderer.display_code_input(0)
        output = self.held_output.getvalue().strip()
        self.assertIn("Available colors and their codes:", output)

    def test_display_code_input_max_colors(self: "TestMenuRenderer") -> None:
        """Test the display_code_input method.

        with the maximum number of available colors.
        """
        max_colors = len(ColorCode)
        self.renderer.display_code_input(max_colors)
        output = self.held_output.getvalue().strip()
        self.assertIn("Available colors and their codes:", output)
        for color in ColorCode:
            self.assertIn(f"{color.value}: {color}", output)

    def test_display_code_input_invalid_color(self: "TestMenuRenderer") -> None:
        """Test the display_code_input method with an invalid color code."""
        invalid_color = "invalid"
        with self.assertRaises(ValueError):
            self.renderer.display_code_input(invalid_color)

    def test_display_ingame_menu_invalid_type(self: "TestMenuRenderer") -> None:
        """Test the display_ingame_menu method.

        with an invalid type for available actions.
        """
        invalid_actions = "invalid"
        with self.assertRaises(ValueError):
            self.renderer.display_ingame_menu(invalid_actions)


if __name__ == "__main__":
    unittest.main()
