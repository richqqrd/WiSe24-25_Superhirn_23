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
    def test_run_choose_mode(self, mock_input, mock_menu, mock_clear):
        mock_input.side_effect = ["choose_mode", "end_game"]
        self.mock_logic.handle.side_effect = ["choose_mode", "end_game"]

        with patch.object(self.console, 'handle_game_mode_choice') as mock_handle_game_mode_choice:
            self.console.run()
            mock_handle_game_mode_choice.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_choose_language(self, mock_input, mock_menu, mock_clear):
        mock_input.side_effect = ["choose_language", "end_game"]
        self.mock_logic.handle.side_effect = ["choose_language", "end_game"]

        with patch.object(self.console, 'handle_language_change') as mock_handle_language_change:
            self.console.run()
            mock_handle_language_change.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_save_game(self, mock_input, mock_menu, mock_clear):
        mock_input.side_effect = ["save_game", "end_game"]
        self.mock_logic.handle.side_effect = ["save_game", "end_game"]

        with patch.object(self.console.application_logic, 'save_game') as mock_save_game, \
                patch.object(self.console.menu_renderer, 'display_save_game') as mock_display_save_game:
            self.console.run()
            mock_save_game.assert_called_once()
            mock_display_save_game.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_load_game(self, mock_input, mock_menu, mock_clear):
        mock_input.side_effect = ["load_game", "end_game"]
        self.mock_logic.handle.side_effect = ["load_game", "end_game"]
        self.mock_logic.load_game.return_value = "next_action"

        with patch.object(self.console, 'start_game_loop') as mock_start_game_loop:
            self.console.run()
            mock_start_game_loop.assert_called_once_with("next_action")

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_choose_mode(self, mock_input, mock_menu, mock_clear):
        mock_input.side_effect = ["choose_mode", "end_game"]
        self.mock_logic.handle.side_effect = ["choose_mode", "end_game"]

        with patch.object(self.console, 'handle_game_mode_choice') as mock_handle_game_mode_choice:
            self.console.run()
            mock_handle_game_mode_choice.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_choose_language(self, mock_input, mock_menu, mock_clear):
        mock_input.side_effect = ["choose_language", "end_game"]
        self.mock_logic.handle.side_effect = ["choose_language", "end_game"]

        with patch.object(self.console, 'handle_language_change') as mock_handle_language_change:
            self.console.run()
            mock_handle_language_change.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_save_game(self, mock_input, mock_menu, mock_clear):
        mock_input.side_effect = ["save_game", "end_game"]
        self.mock_logic.handle.side_effect = ["save_game", "end_game"]

        with patch.object(self.console.application_logic, 'save_game') as mock_save_game, \
                patch.object(self.console.menu_renderer, 'display_save_game') as mock_display_save_game:
            self.console.run()
            mock_save_game.assert_called_once()
            mock_display_save_game.assert_called_once()

    # @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    # @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    # @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    # def test_run_resume_game(self, mock_input, mock_menu, mock_clear):
    #     mock_input.side_effect = ["resume_game", "end_game"]
    #     self.mock_logic.handle.side_effect = ["resume_game", "end_game"]
    #     self.mock_logic.load_game.return_value = "next_action"
    #
    #     with patch.object(self.console, 'start_game_loop') as mock_start_game_loop:
    #         self.console.run()
    #         mock_start_game_loop.assert_called_once_with("next_action")

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

    def test_end_game(self):
        self.console.end_game()
        self.assertFalse(self.console.is_game_active)

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_ingame_menu")
    def test_handle_ingame_menu(self, mock_display_menu, mock_handle_input):
        self.mock_logic.get_available_menu_actions.return_value = ["save_game", "end_game"]
        mock_handle_input.side_effect = ["save_game", "end_game"]
        self.mock_logic.handle_menu_action.side_effect = ["save_game", "end_game"]
        self.mock_logic.get_current_game_action.return_value = "game_over"

        next_action = self.console.handle_ingame_menu()

        mock_display_menu.assert_called_once_with(["save_game", "end_game"])
        mock_handle_input.assert_called()
        self.mock_logic.handle_menu_action.assert_called_with("save_game")
        self.assertEqual(next_action, "game_over")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_save_warning_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_save_warning")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_ingame_menu")
    def test_handle_ingame_menu_save_warning(self, mock_display_menu, mock_handle_input, mock_display_warning, mock_handle_warning_input):
        self.mock_logic.get_available_menu_actions.return_value = ["save_game", "end_game"]
        mock_handle_input.side_effect = ["save_game", "end_game"]
        self.mock_logic.handle_menu_action.side_effect = ["confirm_save", "end_game"]
        mock_handle_warning_input.return_value = True
        self.mock_logic.confirm_save_game.return_value = "save_game"
        self.mock_logic.get_current_game_action.return_value = "game_over"

        next_action = self.console.handle_ingame_menu()

        mock_display_menu.assert_called_once_with(["save_game", "end_game"])
        mock_handle_input.assert_called()
        self.mock_logic.handle_menu_action.assert_called_with("save_game")
        mock_display_warning.assert_called_once()
        mock_handle_warning_input.assert_called_once()
        self.mock_logic.confirm_save_game.assert_called_once()
        self.assertEqual(next_action, "game_over")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_save_warning_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_save_warning")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_ingame_menu")
    def test_handle_ingame_menu_save_warning_decline(self, mock_display_menu, mock_handle_input, mock_display_warning, mock_handle_warning_input):
        self.mock_logic.get_available_menu_actions.return_value = ["save_game", "end_game"]
        mock_handle_input.side_effect = ["save_game", "end_game"]
        self.mock_logic.handle_menu_action.side_effect = ["confirm_save", "end_game"]
        mock_handle_warning_input.return_value = False
        self.mock_logic.get_current_game_action.return_value = "continue_game"

        next_action = self.console.handle_ingame_menu()

        mock_display_menu.assert_called_once_with(["save_game", "end_game"])
        mock_handle_input.assert_called()
        self.mock_logic.handle_menu_action.assert_called_with("save_game")
        mock_display_warning.assert_called_once()
        mock_handle_warning_input.assert_called_once()
        self.assertEqual(next_action, "continue_game")

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_load_game")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_ingame_menu")
    def test_handle_ingame_menu_load_game(self, mock_display_menu, mock_handle_input, mock_display_load_game):
        self.mock_logic.get_available_menu_actions.return_value = ["load_game"]
        mock_handle_input.return_value = "load_game"
        self.mock_logic.handle_menu_action.return_value = "load_game"
        self.mock_logic.get_current_game_action.return_value = "game_over"

        next_action = self.console.handle_ingame_menu()

        mock_display_menu.assert_called_once_with(["load_game"])
        mock_handle_input.assert_called_once()
        self.mock_logic.handle_menu_action.assert_called_with("load_game")
        mock_display_load_game.assert_called_once()
        self.assertEqual(next_action, "game_over")

    @patch("src.cli.console.Console.end_game")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_ingame_menu")
    def test_handle_ingame_menu_end_game(self, mock_display_menu, mock_handle_input, mock_end_game):
        self.mock_logic.get_available_menu_actions.return_value = ["end_game"]
        mock_handle_input.return_value = "end_game"
        self.mock_logic.handle_menu_action.return_value = "end_game"

        next_action = self.console.handle_ingame_menu()

        mock_display_menu.assert_called_once_with(["end_game"])
        mock_handle_input.assert_called_once()
        self.mock_logic.handle_menu_action.assert_called_with("end_game")
        mock_end_game.assert_called_once()
        self.assertEqual(next_action, "back_to_menu")

    @patch("src.cli.console.Console.handle_language_change")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_ingame_menu")
    def test_handle_ingame_menu_choose_language(self, mock_display_menu, mock_handle_input, mock_handle_language_change):
        self.mock_logic.get_available_menu_actions.return_value = ["choose_language"]
        mock_handle_input.return_value = "choose_language"
        self.mock_logic.handle_menu_action.return_value = "choose_language"
        self.mock_logic.get_current_game_action.return_value = "choose_language"

        next_action = self.console.handle_ingame_menu()

        mock_display_menu.assert_called_once_with(["choose_language"])
        mock_handle_input.assert_called_once()
        self.mock_logic.handle_menu_action.assert_called_with("choose_language")
        mock_handle_language_change.assert_called_once()
        self.assertEqual(next_action, "choose_language")

    @patch("src.cli.console.Console.render_game_state")
    @patch("src.cli.console.Console.get_user_input")
    @patch("src.cli.console.Console.handle_ingame_menu")
    def test_start_game_loop_need_guess_input(self, mock_handle_menu, mock_get_input, mock_render_state):
        mock_get_input.return_value = "user_guess"
        self.mock_logic.process_game_action.side_effect = ["need_guess_input", "game_over"]
        self.mock_logic.is_game_over.side_effect = [False, True]

        self.console.start_game_loop("need_guess_input")

        mock_render_state.assert_called()
        mock_get_input.assert_called_with("need_guess_input")
        self.mock_logic.process_game_action.assert_called_with("need_guess_input", "user_guess")

    @patch("src.cli.console.Console.render_game_state")
    @patch("src.cli.console.Console.get_user_input")
    @patch("src.cli.console.Console.handle_ingame_menu")
    def test_start_game_loop_show_menu(self, mock_handle_menu, mock_get_input, mock_render_state):
        mock_get_input.return_value = "user_input"
        self.mock_logic.process_game_action.side_effect = ["show_menu", "game_over"]
        self.mock_logic.is_game_over.side_effect = [False, True]
        mock_handle_menu.return_value = "next_action"

        self.console.start_game_loop("show_menu")

        mock_handle_menu.assert_called_once()
        self.mock_logic.process_game_action.assert_called_with("show_menu", "user_input")

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_game_won")
    def test_handle_game_end_game_won(self, mock_display_game_won):
        self.console.handle_game_end("game_won")
        mock_display_game_won.assert_called_once()

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_game_lost")
    def test_handle_game_end_game_lost(self, mock_display_game_lost):
        self.console.handle_game_end("game_lost")
        mock_display_game_lost.assert_called_once()

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_cheating_warning")
    def test_handle_game_end_cheating_detected(self, mock_display_cheating_warning):
        self.console.handle_game_end("cheating_detected")
        mock_display_cheating_warning.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.render_game_state")
    def test_render_game_state(self, mock_render_game_state):
        mock_game_state = MagicMock()
        self.mock_logic.get_game_state.return_value = mock_game_state

        self.console.render_game_state()

        mock_render_game_state.assert_called_once_with(mock_game_state)

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_guess_input")
    def test_get_user_input_need_guess_input(self, mock_handle_guess_input):
        mock_handle_guess_input.return_value = "user_guess"
        self.mock_logic.get_positions.return_value = 4

        result = self.console.get_user_input("need_guess_input")

        mock_handle_guess_input.assert_called_once_with(4)
        self.assertEqual(result, "user_guess")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_code_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_code_input")
    def test_get_user_input_need_code_input(self, mock_display_code_input, mock_handle_code_input):
        mock_handle_code_input.return_value = "user_code"
        self.mock_logic.get_positions.return_value = 4
        self.mock_logic.get_colors.return_value = ["red", "blue", "green"]

        result = self.console.get_user_input("need_code_input")

        mock_display_code_input.assert_called_once_with(["red", "blue", "green"])
        mock_handle_code_input.assert_called_once_with(4)
        self.assertEqual(result, "user_code")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_feedback_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_feedback_instructions")
    def test_get_user_input_need_feedback_input(self, mock_display_feedback_instructions, mock_handle_feedback_input):
        mock_handle_feedback_input.return_value = "user_feedback"
        self.mock_logic.get_positions.return_value = 4

        result = self.console.get_user_input("need_feedback_input")

        mock_display_feedback_instructions.assert_called_once()
        mock_handle_feedback_input.assert_called_once_with(4)
        self.assertEqual(result, "user_feedback")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_ip_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_port_input")
    def test_get_user_input_need_server_connection(self, mock_handle_port_input, mock_handle_ip_input):
        mock_handle_ip_input.return_value = "127.0.0.1"
        mock_handle_port_input.return_value = "8080"

        result = self.console.get_user_input("need_server_connection")

        mock_handle_ip_input.assert_called_once()
        mock_handle_port_input.assert_called_once()
        self.assertEqual(result, "127.0.0.1:8080")

    def test_get_user_input_default_case(self):
        result = self.console.get_user_input("unknown_action")
        self.assertEqual(result, "")

    @patch("src.cli.console.Console.collect_game_configuration")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_invalid_configuration")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_game_mode_input")
    def test_handle_game_mode_choice_invalid_configuration(self, mock_handle_game_mode_input, mock_display_invalid_configuration, mock_collect_game_configuration):
        self.mock_logic.get_required_action.return_value = "need_configuration"
        self.mock_logic.configure_game.side_effect = ["invalid_configuration", "start_game"]
        mock_collect_game_configuration.return_value = {"config_key": "config_value"}
        mock_handle_game_mode_input.return_value = "single_player"

        with patch.object(self.console, 'start_game_loop') as mock_start_game_loop:
            self.console.handle_game_mode_choice()
            mock_display_invalid_configuration.assert_called_once()
            self.assertEqual(self.mock_logic.configure_game.call_count, 2)
            mock_start_game_loop.assert_called_once_with("start_game")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_player_name_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_positions_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_colors_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_max_attempts_input")
    def test_collect_game_configuration(self, mock_handle_max_attempts_input, mock_handle_colors_input, mock_handle_positions_input, mock_handle_player_name_input):
        mock_handle_player_name_input.return_value = "TestPlayer"
        mock_handle_positions_input.return_value = 4
        mock_handle_colors_input.return_value = ["red", "blue", "green", "yellow"]
        mock_handle_max_attempts_input.return_value = 10

        config = self.console.collect_game_configuration()

        self.assertEqual(config, {
            "player_name": "TestPlayer",
            "positions": 4,
            "colors": ["red", "blue", "green", "yellow"],
            "max_attempts": 10
        })

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_game_mode_input")
    def test_invalid_game_mode(self, mock_handle_game_mode_input):
        mock_handle_game_mode_input.return_value = "invalid_mode"
        self.mock_logic.get_required_action.return_value = "error"

        self.console.handle_game_mode_choice()

        self.mock_logic.get_required_action.assert_called_with("invalid_mode")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_language_input")
    def test_invalid_language_selection(self, mock_handle_language_input):
        mock_handle_language_input.return_value = "invalid_language"

        self.console.handle_language_change()

        self.assertNotEqual(self.console.menu_renderer.language, "invalid_language")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_player_name_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_positions_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_colors_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_max_attempts_input")
    def test_incomplete_game_configuration(self, mock_handle_max_attempts_input, mock_handle_colors_input, mock_handle_positions_input, mock_handle_player_name_input):
        mock_handle_player_name_input.return_value = "TestPlayer"
        mock_handle_positions_input.return_value = 4
        mock_handle_colors_input.return_value = []
        mock_handle_max_attempts_input.return_value = 10

        config = self.console.collect_game_configuration()

        self.assertEqual(config["colors"], [])


if __name__ == "__main__":
    unittest.main()