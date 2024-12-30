# tests/CLI/menu_renderer/test_menu_renderer.py
import unittest
from io import StringIO
import sys
from src.CLI.menu_renderer.menu_renderer import MenuRenderer
from src.util.ColorCode import ColorCode


class TestMenuRenderer(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment by redirecting stdout.
        """
        self.renderer = MenuRenderer()
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """
        Restore stdout after the test.
        """
        sys.stdout = sys.__stdout__

    def test_display_menu(self):
        """
        Test the display_menu method to ensure it
        correctly displays the menu.
        """
        self.renderer.display_main_menu()
        output = self.held_output.getvalue().strip()
        self.assertIn("Main Menu", output)
        self.assertIn("1. Start Offline Game", output)
        self.assertIn("2. Start Online Game", output)
        self.assertIn("3. Change Language", output)
        self.assertIn("4. End Game", output)
        self.assertIn("5. Save Game", output)
        self.assertIn("6. Resume Interrupted Game", output)

    def test_display_role_menu(self):
        """
        Test the display_role_menu method to ensure it
        correctly displays the role menu.
        """
        self.renderer.display_role_menu()
        output = self.held_output.getvalue().strip()
        self.assertIn("Select your role:", output)
        self.assertIn("1. Guesser", output)
        self.assertIn("2. Coder", output)

    def test_display_languages(self):
        """
        Test the display_languages method to ensure it
        correctly displays the language menu.
        """
        self.renderer.display_languages()
        output = self.held_output.getvalue().strip()
        self.assertIn("Select a language:", output)
        self.assertIn("1. German", output)
        self.assertIn("2. English", output)

    def test_display_end_game(self):
        """
        Test the display_end_game method to ensure it
        correctly displays the end game message.
        """
        self.renderer.display_end_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game ended.", output)

    def test_display_save_game(self):
        """
        Test the display_save_game method to ensure it
        correctly displays the save game message.
        """
        self.renderer.display_save_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game saved.", output)

    def test_display_resume_game(self):
        """
        Test the display_resume_game method to ensure it
        correctly displays the resume game message.
        """
        self.renderer.display_load_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("loads resumed game", output)

    def test_display_start_game(self):
        """
        Test the display_start_game method to ensure it
        correctly displays the start game message.
        """
        self.renderer.display_start_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game started.", output)

    def test_display_code_input(self):
        """
        Test the display_code_input method to ensure it
        correctly displays the code input.
        """
        self.renderer.display_code_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Available colors and their codes:", output)
        for color in ColorCode:
            self.assertIn(f"{color.value} : {color}", output)

    def test_display_guess_input(self):
        """
        Test the display_guess_input method to ensure it
        correctly displays the guess input.
        """
        self.renderer.display_guess_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Available colors and their codes:", output)
        for color in ColorCode:
            self.assertIn(f"{color.value} : {color}", output)

    def test_display_feedback_input(self):
        """
        Test the display_feedback_input method to ensure it
        correctly displays the feedback input.
        """
        self.renderer.display_feedback_input()
        output = self.held_output.getvalue().strip()
        self.assertIn("Give feedback for the guess:", output)
        self.assertIn("8: Black (correct color in correct position)", output)
        self.assertIn("7: White (correct color in wrong position)", output)
        self.assertIn("Enter feedback (e.g. 887 for two black, one white):", output)


if __name__ == "__main__":
    unittest.main()
