"""Test cases for the Console class."""
import unittest
from unittest.mock import MagicMock, patch, DEFAULT
from src.cli.console import Console
from src.application_logic.i_application_logic import IApplicationLogic


class TestConsole(unittest.TestCase):
    """Test cases for the Console class."""
    def setUp(self: "TestConsole") -> None:
        """Set up test fixtures before each test method."""
        self.mock_logic = MagicMock(spec=IApplicationLogic)
        self.mock_logic.business_logic = MagicMock()
        self.console = Console(self.mock_logic)

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_choose_mode(self: "TestConsole", mock_input: MagicMock,
                             mock_menu: MagicMock, mock_clear: MagicMock) -> None:
        """Test run method with choose_mode action."""
        mock_input.side_effect = ["choose_mode", "end_game"]
        self.mock_logic.handle.side_effect = ["choose_mode", "end_game"]

        with (patch.object(self.console, 'handle_game_mode_choice')
              as mock_handle_game_mode_choice):
            self.console.run()
            mock_handle_game_mode_choice.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_choose_language(self: "TestConsole", mock_input: MagicMock,
                                 mock_menu: MagicMock, mock_clear: MagicMock) -> None:
        """Test run method with choose_language action."""
        mock_input.side_effect = ["choose_language", "end_game"]
        self.mock_logic.handle.side_effect = ["choose_language", "end_game"]

        with (patch.object(self.console, 'handle_language_change')
              as mock_handle_language_change):
            self.console.run()
            mock_handle_language_change.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_save_game(self: "TestConsole", mock_input: MagicMock,
                           mock_menu: MagicMock, mock_clear: MagicMock) -> None:
        """Test run method with save_game action."""
        mock_input.side_effect = ["save_game", "end_game"]
        self.mock_logic.handle.side_effect = ["save_game", "end_game"]

        with (patch.object(self.console.application_logic, 'save_game')
                as mock_save_game,
                patch.object(self.console.menu_renderer, 'display_save_game')
                as mock_display_save_game):
            self.console.run()
            mock_save_game.assert_called_once()
            mock_display_save_game.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_resume_game(self: "TestConsole", mock_input: MagicMock,
                             mock_menu: MagicMock, mock_clear: MagicMock) -> None:
        """Test run method with resume_game action."""
        mock_input.side_effect = ["resume_game", "end_game"]
        self.mock_logic.handle.side_effect = ["resume_game", "end_game"]

        with (patch.object(self.console, 'handle_ingame_menu')
              as mock_handle_ingame_menu):
            self.console.run()
            mock_handle_ingame_menu.assert_called_once()

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_languages")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_language_input")
    def test_handle_language_change(self: "TestConsole",
                                    mock_lang_input: MagicMock,
                                    mock_display: MagicMock) -> None:
        """Test handle_language_change method."""
        mock_lang_input.return_value = "de"
        self.console.menu_renderer.language = "de"

        self.console.handle_language_change()

        self.assertEqual(self.console.menu_renderer.language, "de")
        mock_display.assert_called()
        mock_lang_input.assert_called_with("de")

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_game_mode_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_game_mode_input")
    def test_handle_game_mode_choice(self: "TestConsole",
                                     mock_game_input: MagicMock,
                                     mock_display_mode: MagicMock) -> None:
        """Test handle_game_mode_choice method."""
        mock_game_input.return_value = "single_player"
        self.mock_logic.get_required_action.return_value = "start_game"

        self.console.handle_game_mode_choice()

        mock_display_mode.assert_called()
        mock_game_input.assert_called()
        self.mock_logic.get_required_action.assert_called_with("single_player")

    def test_end_game(self: "TestConsole") -> None:
        """Test end_game method."""
        self.console.end_game()
        self.assertFalse(self.console.is_game_active)

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_ingame_menu")
    def test_handle_ingame_menu(self: "TestConsole",
                                mock_display_menu: MagicMock,
                                mock_handle_input: MagicMock) -> None:
        """Test handle_ingame_menu method."""
        self.mock_logic.get_available_menu_actions.return_value =\
            ["save_game", "end_game"]
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
    def test_handle_ingame_menu_save_warning(self: "TestConsole",
                                             mock_display_menu: MagicMock,
                                             mock_handle_input: MagicMock,
                                             mock_display_warning: MagicMock,
                                             mock_handle_warning_input:
                                             MagicMock) -> None:
        """Test handle_ingame_menu method with save warning."""
        self.mock_logic.get_available_menu_actions.return_value =\
            ["save_game", "end_game"]
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
    def test_handle_ingame_menu_save_warning_decline(self: "TestConsole",
                                                     mock_display_menu: MagicMock,
                                                     mock_handle_input: MagicMock,
                                                     mock_display_warning: MagicMock,
                                                     mock_handle_warning_input:
                                                     MagicMock) -> None:
        """Test handle_ingame_menu method with declined save warning."""
        self.mock_logic.get_available_menu_actions.return_value =\
            ["save_game", "end_game"]
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
    def test_handle_ingame_menu_load_game(self: "TestConsole",
                                          mock_display_menu: MagicMock,
                                          mock_handle_input: MagicMock,
                                          mock_display_load_game: MagicMock) -> None:
        """Test handle_ingame_menu method with load game action."""
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
    def test_handle_ingame_menu_end_game(self: "TestConsole",
                                         mock_display_menu: MagicMock,
                                         mock_handle_input: MagicMock,
                                         mock_end_game: MagicMock) -> None:
        """Test handle_ingame_menu method with end game action."""
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
    def test_handle_ingame_menu_choose_language(self: "TestConsole",
                                                mock_display_menu: MagicMock,
                                                mock_handle_input: MagicMock,
                                                mock_handle_language_change:
                                                MagicMock) -> None:
        """Test handle_ingame_menu method with choose language action."""
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
    def test_start_game_loop_need_guess_input(self: "TestConsole",
                                              mock_handle_menu: MagicMock,
                                              mock_get_input: MagicMock,
                                              mock_render_state: MagicMock) -> None:
        """Test start_game_loop method with need_guess_input action."""
        mock_get_input.return_value = "user_guess"
        self.mock_logic.process_game_action.side_effect = ["need_guess_input",
                                                           "game_over"]
        self.mock_logic.is_game_over.side_effect = [False, True]

        self.console.start_game_loop("need_guess_input")

        mock_render_state.assert_called()
        mock_get_input.assert_called_with("need_guess_input")
        self.mock_logic.process_game_action.assert_called_with("need_guess_input",
                                                               "user_guess")

    @patch("src.cli.console.Console.render_game_state")
    @patch("src.cli.console.Console.get_user_input")
    @patch("src.cli.console.Console.handle_ingame_menu")
    def test_start_game_loop_show_menu(self: "TestConsole",
                                       mock_handle_menu: MagicMock,
                                       mock_get_input: MagicMock) -> None:
        """Test start_game_loop method with show_menu action."""
        mock_get_input.return_value = "user_input"
        self.mock_logic.process_game_action.side_effect = ["show_menu", "game_over"]
        self.mock_logic.is_game_over.side_effect = [False, True]
        mock_handle_menu.return_value = "next_action"

        self.console.start_game_loop("show_menu")

        mock_handle_menu.assert_called_once()
        self.mock_logic.process_game_action.assert_called_with("show_menu",
                                                               "user_input")

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_game_won")
    def test_handle_game_end_game_won(self: "TestConsole",
                                      mock_display_game_won: MagicMock) -> None:
        """Test handle_game_end method with game_won action."""
        self.console.handle_game_end("game_won")
        mock_display_game_won.assert_called_once()

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_game_lost")
    def test_handle_game_end_game_lost(self: "TestConsole",
                                       mock_display_game_lost: MagicMock) -> None:
        """Test handle_game_end method with game_lost action."""
        self.console.handle_game_end("game_lost")
        mock_display_game_lost.assert_called_once()

    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_cheating_warning")
    def test_handle_game_end_cheating_detected(self: "TestConsole",
                                               mock_display_cheating_warning:
                                               MagicMock) -> None:
        """Test handle_game_end method with cheating_detected action."""
        self.console.handle_game_end("cheating_detected")
        mock_display_cheating_warning.assert_called_once()

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.render_game_state")
    def test_render_game_state(self: "TestConsole",
                               mock_render_game_state: MagicMock) -> None:
        """Test render_game_state method."""
        mock_game_state = MagicMock()
        self.mock_logic.get_game_state.return_value = mock_game_state

        self.console.render_game_state()

        mock_render_game_state.assert_called_once_with(mock_game_state)

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_guess_input")
    def test_get_user_input_need_guess_input(self: "TestConsole",
                                             mock_handle_guess_input:
                                             MagicMock) -> None:
        """Test get_user_input method with need_guess_input action."""
        mock_handle_guess_input.return_value = "user_guess"
        self.mock_logic.get_positions.return_value = 4

        result = self.console.get_user_input("need_guess_input")

        mock_handle_guess_input.assert_called_once_with(4)
        self.assertEqual(result, "user_guess")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_code_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_code_input")
    def test_get_user_input_need_code_input(self: "TestConsole",
                                            mock_display_code_input: MagicMock,
                                            mock_handle_code_input: MagicMock) -> None:
        """Test get_user_input method with need_code_input action."""
        mock_handle_code_input.return_value = "user_code"
        self.mock_logic.get_positions.return_value = 4
        self.mock_logic.get_colors.return_value = ["red", "blue", "green"]

        result = self.console.get_user_input("need_code_input")

        mock_display_code_input.assert_called_once_with(["red", "blue", "green"])
        mock_handle_code_input.assert_called_once_with(4)
        self.assertEqual(result, "user_code")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_feedback_input")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer."
           "display_feedback_instructions")
    def test_get_user_input_need_feedback_input(self: "TestConsole",
                                                mock_display_feedback_instructions:
                                                MagicMock,
                                                mock_handle_feedback_input:
                                                MagicMock) -> None:
        """Test get_user_input method with need_feedback_input action."""
        mock_handle_feedback_input.return_value = "user_feedback"
        self.mock_logic.get_positions.return_value = 4

        result = self.console.get_user_input("need_feedback_input")

        mock_display_feedback_instructions.assert_called_once()
        mock_handle_feedback_input.assert_called_once_with(4)
        self.assertEqual(result, "user_feedback")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_ip_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_port_input")
    def test_get_user_input_need_server_connection(self: "TestConsole",
                                                   mock_handle_port_input: MagicMock,
                                                   mock_handle_ip_input:
                                                   MagicMock) -> None:
        """Test get_user_input method with need_server_connection action."""
        mock_handle_ip_input.return_value = "127.0.0.1"
        mock_handle_port_input.return_value = "8080"

        result = self.console.get_user_input("need_server_connection")

        mock_handle_ip_input.assert_called_once()
        mock_handle_port_input.assert_called_once()
        self.assertEqual(result, "127.0.0.1:8080")

    def test_get_user_input_default_case(self: "TestConsole") -> None:
        """Test get_user_input method with default case."""
        result = self.console.get_user_input("unknown_action")
        self.assertEqual(result, "")

    @patch("src.cli.console.Console.collect_game_configuration")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer."
           "display_invalid_configuration")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_game_mode_input")
    def test_handle_game_mode_choice_invalid_config(self: "TestConsole",
                                                    mock_handle_game_mode_input:
                                                    MagicMock,
                                                    mock_display_invalid_configuration:
                                                    MagicMock,
                                                    mock_collect_game_configuration:
                                                    MagicMock) -> None:
        """Test handle_game_mode_choice method with invalid configuration."""
        self.mock_logic.get_required_action.return_value = "need_configuration"
        self.mock_logic.configure_game.side_effect =\
            ["invalid_configuration", "start_game"]
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
    def test_collect_game_configuration(self: "TestConsole",
                                        mock_handle_max_attempts_input: MagicMock,
                                        mock_handle_colors_input: MagicMock,
                                        mock_handle_positions_input: MagicMock,
                                        mock_handle_player_name_input: MagicMock)\
            -> None:
        """Test collect_game_configuration method."""
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
    def test_invalid_game_mode(self: "TestConsole",
                               mock_handle_game_mode_input: MagicMock) -> None:
        """Test handle_game_mode_choice method with invalid game mode."""
        mock_handle_game_mode_input.return_value = "invalid_mode"
        self.mock_logic.get_required_action.return_value = "error"

        self.console.handle_game_mode_choice()

        self.mock_logic.get_required_action.assert_called_with("invalid_mode")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_language_input")
    def test_invalid_language_selection(self: "TestConsole",
                                        mock_handle_language_input: MagicMock) -> None:
        """Test handle_language_change method with invalid language selection."""
        mock_handle_language_input.return_value = "invalid_language"

        self.console.handle_language_change()

        self.assertNotEqual(self.console.menu_renderer.language, "invalid_language")

    @patch("src.cli.input_handler.input_handler.InputHandler.handle_player_name_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_positions_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_colors_input")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_max_attempts_input")
    def test_incomplete_game_configuration(self: "TestConsole",
                                           mock_handle_max_attempts_input: MagicMock,
                                           mock_handle_colors_input: MagicMock,
                                           mock_handle_positions_input: MagicMock,
                                           mock_handle_player_name_input: MagicMock)\
            -> None:
        """Test collect_game_configuration method with incomplete configuration."""
        mock_handle_player_name_input.return_value = "TestPlayer"
        mock_handle_positions_input.return_value = 4
        mock_handle_colors_input.return_value = []
        mock_handle_max_attempts_input.return_value = 10

        config = self.console.collect_game_configuration()

        self.assertEqual(config["colors"], [])

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_load_game(self: "TestConsole", mock_input: MagicMock,
                           mock_menu: MagicMock, mock_clear: MagicMock) -> None:
        """Test load game path in run method."""
        # Setup
        mock_input.side_effect = ["load_game", "end_game"]
        self.mock_logic.handle.side_effect = ["load_game", "end_game"]
        self.mock_logic.load_game.side_effect = ["need_guess_input"]

        # Execute
        with patch.object(self.console, 'start_game_loop') as mock_start_game_loop:
            self.console.run()

            # Verify
            mock_start_game_loop.assert_called_once_with("need_guess_input")

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_complete(self: "TestConsole", mock_input: MagicMock,
                          mock_menu: MagicMock, mock_clear: MagicMock) -> None:
        """Test complete run method with all possible actions."""
        # Setup
        mock_input.side_effect = [
            "1",  # choose_mode
            "2",  # choose_language
            "3",  # save_game
            "4"  # end_game
        ]

        self.mock_logic.handle.side_effect = [
            "choose_mode",
            "choose_language",
            "save_game",
            "end_game"
        ]

        self.mock_logic.get_available_menu_actions.return_value = [
            "save_game", "change_language", "end_game"
        ]

        # Execute
        with patch.multiple(self.console,
                            handle_game_mode_choice=DEFAULT,
                            handle_language_change=DEFAULT) as mocks:
            self.console.run()

            # Verify calls
            mocks["handle_game_mode_choice"].assert_called_once()
            mocks["handle_language_change"].assert_called_once()
            self.mock_logic.save_game.assert_called_once()
            self.assertFalse(self.console.is_game_active)

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_invalid_action(self: "TestConsole", mock_input: MagicMock,
                                mock_menu: MagicMock, mock_clear: MagicMock) -> None:
        """Test run method with invalid action."""
        mock_input.side_effect = ["invalid", "end_game"]
        self.mock_logic.handle.side_effect = ["invalid", "end_game"]

        self.console.run()

        mock_menu.assert_called()
        self.assertFalse(self.console.is_game_active)

    @patch("src.cli.game_renderer.game_renderer.GameRenderer.clear_screen")
    @patch("src.cli.menu_renderer.menu_renderer.MenuRenderer.display_main_menu")
    @patch("src.cli.input_handler.input_handler.InputHandler.handle_menu_input")
    def test_run_save_load_game(self: "TestConsole", mock_input: MagicMock,
                                mock_menu: MagicMock, mock_clear: MagicMock) -> None:
        """Test run method with save and load game."""
        # Setup
        mock_input.side_effect =\
            ["save_game", "load_game", "end_game"]  # Änderung hier
        self.mock_logic.handle.side_effect =\
            ["save_game", "load_game", "end_game"]  # Und hier
        self.mock_logic.get_available_menu_actions.return_value =\
            ["save_game", "load_game"]
        self.mock_logic.load_game.return_value = "need_guess_input"

        # Execute
        with patch.object(self.console, 'start_game_loop') as mock_start_game_loop:
            self.console.run()

            # Verify
            self.mock_logic.save_game.assert_called_once()
            self.mock_logic.load_game.assert_called_once()
            mock_start_game_loop.assert_called_once_with("need_guess_input")
            self.assertFalse(self.console.is_game_active)


if __name__ == "__main__":
    unittest.main()
