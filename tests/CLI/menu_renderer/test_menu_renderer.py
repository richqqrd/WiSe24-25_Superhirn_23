import unittest
from io import StringIO
import sys
from src.CLI.menu_renderer.menu_renderer import MenuRenderer


class TestMenuRenderer(unittest.TestCase):

    def setUp(self):
        """Set up the test environment by redirecting stdout."""
        self.renderer = MenuRenderer()
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        """Restore stdout after the test."""
        sys.stdout = sys.__stdout__

    def test_display_menu(self):
        """Test the display_menu method to ensure it correctly displays the menu."""
        self.renderer.display_menu()
        output = self.held_output.getvalue().strip()
        self.assertIn("Main Menu", output)
        self.assertIn("1. Start Offline Game", output)
        self.assertIn("2. Start Online Game", output)
        self.assertIn("3. Change Language", output)
        self.assertIn("4. End Game", output)
        self.assertIn("5. Save Game", output)
        self.assertIn("6. Resume Interrupted Game", output)

    def test_change_language(self):
        """Test the change_language method to ensure it correctly handles the option."""
        self.renderer.change_language()
        output = self.held_output.getvalue().strip()
        self.assertIn("Language changed.", output)

    def test_end_game(self):
        """Test the end_game method to ensure it correctly handles the option."""
        self.renderer.end_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game ended.", output)

    def test_save_game(self):
        """Test the save_game method to ensure it correctly handles the option."""
        self.renderer.save_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game saved.", output)

    def test_start_game(self):
        """Test the start_game method to ensure it correctly handles the option."""
        self.renderer.start_offline_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("1. Play as Guesser", output)
        self.assertIn("2. Play as Coder", output)

    def test_start_online_game(self):
        """Test the start_online_game method to ensure it correctly handles the option."""
        self.renderer.start_online_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game started.", output)

    def test_resume_interrupted_game(self):
        """Test the resume_interrupted_game method to ensure it correctly handles the option."""
        self.renderer.resume_interrupted_game()
        output = self.held_output.getvalue().strip()
        self.assertIn("Resumed interrupted game.", output)

    def test_start_offline_game_as_guesser(self):
        """Test the start_offline_game method to ensure it correctly handles the option."""
        self.renderer.start_offline_game_as_guesser()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game started as Guesser.", output)

    def test_start_offline_game_as_coder(self):
        """Test the start_offline_game method to ensure it correctly handles the option."""
        self.renderer.start_offline_game_as_coder()
        output = self.held_output.getvalue().strip()
        self.assertIn("Game started as Coder.", output)


if __name__ == '__main__':
    unittest.main()