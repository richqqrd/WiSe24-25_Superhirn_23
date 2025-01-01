"""Module for console-based user interface."""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.business_logic.i_business_logic import IBusinessLogic
from src.cli.game_renderer.game_renderer import GameRenderer
from src.cli.input_handler.input_handler import InputHandler
from src.cli.menu_renderer.menu_renderer import MenuRenderer


class Console:
    """Main console interface controller.

    This class coordinates all user interface components and handles
    the main game loop.

    Attributes:
        business_logic: Business logic layer interface
        menu_renderer: Renderer for menus
        game_renderer: Renderer for game states
        input_handler: Handler for user input
        is_game_active: Flag indicating if game is running
    """

    def __init__(self: "Console", business_logic: IBusinessLogic) -> None:
        """Initialize console interface.

        Args:
            business_logic: Business logic layer interface
        """
        self.business_logic = business_logic
        self.menu_renderer = MenuRenderer()
        self.game_renderer = GameRenderer()
        self.input_handler = InputHandler()
        self.is_game_active = True

    def run(self: "Console") -> None:
        """Run the main application loop.

        Handles main menu navigation and delegates to appropriate handlers.
        """
        while self.is_game_active:
            self.game_renderer.clear_screen()
            self.menu_renderer.display_main_menu()
            user_input = self.input_handler.handle_menu_input()
            action = self.business_logic.handle(user_input)

            if action == "choose_mode":
                self.handle_game_mode_choice()
            elif action == "choose_language":
                self.handle_language_change()
            elif action == "end_game":
                self.end_game()
            elif action == "save_game":
                self.business_logic.save_game()
                self.menu_renderer.display_save_game()
            elif action == "resume_game":
                next_action = self.business_logic.load_game()
                if next_action != "error":
                    self.start_game_loop(next_action)

    def handle_language_change(self: "Console") -> None:
        """Handle language selection and update.

        Displays language options and updates all UI components
        with selected language.
        """
        self.menu_renderer.display_languages()
        language = self.input_handler.handle_language_input(
            self.menu_renderer.language
        )
        self.update_language(language)

    def update_language(self: "Console", language: str) -> None:
        """Update language for all UI components.

        Args:
            language: New language code to set
        """
        self.menu_renderer.set_language(language)
        self.game_renderer.set_language(language)
        self.input_handler.set_language(language)

    def start_game_loop(self: "Console", next_action: str) -> None:
        """Control the main game loop.

        Handles game state rendering and user input processing
        until game is over.

        Args:
            next_action: Initial game action to process
        """
        while not self.business_logic.is_game_over(next_action):

            if next_action in [
                "need_guess_input",
                "need_feedback_input",
                "need_code_input",
                "wait_for_computer_guess",
            ]:
                self.render_game_state()

            user_input = self.get_user_input(next_action)
            next_action = self.business_logic.process_game_action(
                next_action, user_input
            )

            if next_action == "show_menu":
                next_action = self.handle_ingame_menu()

        self.handle_game_end(next_action)

    def handle_game_end(self: "Console", next_action: str) -> None:
        """Handle end of game states.

        Displays final game state and appropriate end message based on:
        - Game won
        - Game lost
        - Cheating detected
        Then ends the game session.
        """
        self.game_renderer.render_game_state(self.business_logic.get_game_state())

        if next_action == "game_won":
            self.menu_renderer.display_game_won()
        elif next_action == "game_lost":
            self.menu_renderer.display_game_lost()
        elif next_action == "cheating_detected":
            self.menu_renderer.display_cheating_warning()
        self.end_game()

    def render_game_state(self: "Console") -> None:
        """Render current game state.

        Displays the current game state using the game renderer,
        including board layout, guesses, and feedback.
        """
        self.game_renderer.render_game_state(self.business_logic.get_game_state())

    def get_user_input(self: "Console", action: str) -> str:
        """Get appropriate user input based on the current game action.

        Args:
            action: The current game action that requires user input

        Returns:
            str: The user input appropriate for the action

        Actions handled:
            - need_guess_input: Get guess from player
            - need_code_input: Get secret code from player
            - need_feedback_input: Get feedback from player
            - need_server_connection: Get server connection details
        """
        if action == "need_guess_input":
            positions = self.business_logic.get_positions()
            return self.input_handler.handle_guess_input(positions)

        elif action == "need_code_input":
            positions = self.business_logic.get_positions()
            colors = self.business_logic.get_colors()
            self.menu_renderer.display_code_input(colors)
            return self.input_handler.handle_code_input(positions)

        elif action == "need_feedback_input":
            positions = self.business_logic.get_positions()
            self.menu_renderer.display_feedback_instructions()
            return self.input_handler.handle_feedback_input(positions)

        elif action == "need_server_connection":
            ip = self.input_handler.handle_ip_input()
            port = self.input_handler.handle_port_input()
            return f"{ip}:{port}"

        return ""

    def handle_ingame_menu(self: "Console") -> str:
        """Handle the in-game menu interactions.

        Displays menu options, processes user input and handles menu actions like:
        - Save game
        - Load game
        - Change language
        - End game

        Returns:
            str: Next game action to process
        """
        available_actions = self.business_logic.get_available_menu_actions()
        self.menu_renderer.display_ingame_menu(available_actions)
        user_input = self.input_handler.handle_menu_input()
        next_action = self.business_logic.handle_menu_action(user_input)

        if next_action == "confirm_save":
            self.menu_renderer.display_save_warning()
            if self.input_handler.handle_save_warning_input():
                next_action = self.business_logic.confirm_save_game()
            else:
                return self.business_logic.get_current_game_action()

        if next_action == "save_game":
            self.menu_renderer.display_save_game()

        elif next_action == "load_game":
            self.menu_renderer.display_load_game()

        elif next_action == "choose_language":
            self.handle_language_change()

        elif next_action == "end_game":
            self.end_game()
            return "game_over"

        return self.business_logic.get_current_game_action()

    def end_game(self: "Console") -> None:
        """End the current game session.

        Displays game end message and sets game inactive.
        """
        self.menu_renderer.display_end_game()
        self.is_game_active = False

    def handle_game_mode_choice(self: "Console") -> None:
        self.game_renderer.clear_screen()
        self.menu_renderer.display_game_mode_menu()
        game_mode = self.input_handler.handle_game_mode_input()

        next_action = self.business_logic.get_required_action(game_mode)

        while next_action == "need_configuration":
            config = self.collect_game_configuration()
            next_action = self.business_logic.configure_game(game_mode, config)

            if next_action == "invalid_configuration":
                self.menu_renderer.display_invalid_configuration()
                next_action = "need_configuration"

        if self.business_logic.can_start_game(next_action):
            self.start_game_loop(next_action)

    def collect_game_configuration(self: "Console") -> dict:
        """Collect game configuration from user input.

        Prompts for and collects:
        - Player name
        - Number of positions
        - Number of colors
        - Maximum attempts

        Returns:
            dict: Game configuration parameters
        """
        self.menu_renderer.display_player_name_input()
        player_name = self.input_handler.handle_player_name_input()
        self.game_renderer.clear_screen()

        self.menu_renderer.display_positions_input()
        positions = self.input_handler.handle_positions_input()
        self.game_renderer.clear_screen()

        self.menu_renderer.display_code_input(8)
        self.menu_renderer.display_colors_input()
        colors = self.input_handler.handle_colors_input()
        self.game_renderer.clear_screen()

        self.menu_renderer.display_max_attempts_input()
        max_attempts = self.input_handler.handle_max_attempts_input()
        self.game_renderer.clear_screen()

        return {
            "player_name": player_name,
            "positions": positions,
            "colors": colors,
            "max_attempts": max_attempts,
        }
