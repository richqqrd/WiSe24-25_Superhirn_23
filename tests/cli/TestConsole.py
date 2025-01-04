import unittest
from unittest.mock import MagicMock, patch
from src.cli.console import Console
from src.application_logic.i_application_logic import IApplicationLogic


class TestConsole(unittest.TestCase):
    def setUp(self):
        self.mock_logic = MagicMock(spec=IApplicationLogic)
        self.console = Console(self.mock_logic)

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_end_game(self, mock_input, mock_menu, mock_clear):
        mock_input.side_effect = ["end_game"]
        self.mock_logic.handle.return_value = "end_game"

        self.console.run()

        self.assertFalse(self.console.is_game_active)
        mock_clear.assert_called()
        mock_menu.assert_called()
        self.mock_logic.handle.assert_called_with("end_game")

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_languages")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_language_input")
    def test_handle_language_change(self, mock_lang_input, mock_display):
        mock_lang_input.return_value = "de"
        self.console.menu_renderer.language = "de"

        self.console.handle_language_change()

        self.assertEqual(self.console.menu_renderer.language, "de")
        mock_display.assert_called()
        mock_lang_input.assert_called_with("de")

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_game_mode_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_game_mode_input")
    def test_handle_game_mode_choice(self, mock_game_input, mock_display_mode):
        mock_game_input.return_value = "single_player"
        self.mock_logic.get_required_action.return_value = "start_game"

        self.console.handle_game_mode_choice()

        mock_display_mode.assert_called()
        mock_game_input.assert_called()
        self.mock_logic.get_required_action.assert_called_with("single_player")

    # @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_save_game")
    # @patch("builtins.input", side_effect=["1"])
    # def test_save_game(self, mock_input, mock_display_save):
    #     self.console.application_logic.save_game.return_value = None
    #     self.mock_logic.get_available_menu_actions.return_value = ["save_game", "load_game"]
    #     self.mock_logic.handle_menu_action.return_value = "save_game"
    #
    #     self.console.handle_ingame_menu()
    #
    #     mock_display_save.assert_called()
    #     self.console.application_logic.save_game.assert_called()
    #
    def test_end_game(self):
        self.console.end_game()
        self.assertFalse(self.console.is_game_active)


if __name__ == "__main__":
    unittest.main()
