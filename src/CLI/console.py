import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.BusinessLogic.IBusinessLogic import IBusinessLogic
from src.CLI.game_renderer.game_renderer import GameRenderer
from src.CLI.input_handler.input_handler import InputHandler
from src.CLI.menu_renderer.menu_renderer import MenuRenderer


class Console:
    def __init__(self, business_logic: IBusinessLogic):
        self.business_logic = business_logic
        self.menu_renderer = MenuRenderer()
        self.game_renderer = GameRenderer()
        self.input_handler = InputHandler()
        self.is_game_active = True

    def run(self) -> None:
        while self.is_game_active:
            self.menu_renderer.display_menu()
            user_input = self.input_handler.handle_menu_input()
            next_action = self.business_logic.handle(user_input)

            if next_action == "choose_role":
                self.handle_game_mode_choice()
            elif next_action in ["end_game", "save_game", "choose_language"]:
                self.handle_menu_action(next_action)

    def handle_game_loop(self, next_action: str) -> None:
        while next_action not in ["game_over", "error", "cheating_detected"]:
            if next_action == "need_guess_input":
                self.game_renderer.render_game_state(
                    self.business_logic.get_game_state()
                )
                guess_input = self.input_handler.handle_guess_input()
                if guess_input == "menu":
                    self.menu_renderer.display_menu()
                    user_input = self.input_handler.handle_menu_input()
                    next_action = self.business_logic.handle(user_input)
                    continue

                next_action = self.business_logic.handle_guess_input(guess_input)
            elif next_action == "need_code_input":
                self.menu_renderer.display_code_input()
                code_input = self.input_handler.handle_code_input()
                if code_input == "menu":
                    self.menu_renderer.display_menu()
                    user_input = self.input_handler.handle_menu_input()
                    next_action = self.business_logic.handle(user_input)
                    continue

                next_action = self.business_logic.handle_code_input(code_input)
            elif next_action == "wait_for_computer_guess":
                next_action = self.business_logic.handle_computer_guess()
                self.game_renderer.render_game_state(
                    self.business_logic.get_game_state()
                )
            elif next_action == "need_server_connection":
                self.menu_renderer.display_server_connection()
                server_ip = self.input_handler.handle_ip_input()
                if server_ip == "menu":
                    self.menu_renderer.display_menu()
                    user_input = self.input_handler.handle_menu_input()
                    next_action = self.business_logic.handle(user_input)
                    continue

                server_port = self.input_handler.handle_port_input()
                if server_port == "menu":
                    self.menu_renderer.display_menu()
                    user_input = self.input_handler.handle_menu_input()
                    next_action = self.business_logic.handle(user_input)
                    continue

                next_action = self.business_logic.handle_server_connection(
                    server_ip, server_port
                )
            elif next_action == "need_feedback_input":
                self.game_renderer.render_game_state(
                    self.business_logic.get_game_state()
                )
                self.menu_renderer.display_feedback_input()
                feedback = self.input_handler.handle_feedback_input()
                if feedback == "menu":
                    self.menu_renderer.display_menu()
                    user_input = self.input_handler.handle_menu_input()
                    next_action = self.business_logic.handle(user_input)

                    continue
                next_action = self.business_logic.handle_feedback_input(feedback)
        if next_action == "game_over":
            self.game_renderer.render_game_state(
                self.business_logic.get_game_state()
            )
            self.end_game()
        elif next_action == "cheating_detected":
            self.menu_renderer.display_cheating_warning()
            self.end_game()
        elif next_action == "error":
            print("error, ending game")
            self.end_game()


    def end_game(self) -> None:
        self.menu_renderer.display_end_game()
        self.is_game_active = False

    def handle_offline_game(self) -> None:
        self.menu_renderer.display_role_menu()
        role_input = self.input_handler.handle_role_input()
        next_action = self.business_logic.handle_role_choice(role_input, "offline")
        self.handle_game_loop(next_action)

    def handle_menu_action(self, action: str) -> None:
        if action == "save_game":
            self.business_logic.save_game()
            self.menu_renderer.display_save_game()
        elif action == "load_game":
            self.business_logic.load_game()
            self.menu_renderer.display_load_game()

        elif action == "choose_language":
            self.menu_renderer.display_languages()
            language_input = self.input_handler.handle_language_input(self.menu_renderer.language)
            self.menu_renderer.set_language(language_input)
            self.input_handler.set_language(language_input)
        elif action == "end_game":
            self.end_game()
    
    def handle_game_mode_choice(self) -> None:
        self.menu_renderer.display_game_mode_menu()
        game_mode = self.input_handler.handle_game_mode_input()
        next_action = self.business_logic.handle_game_mode_choice(game_mode)

        if next_action == "need_configuration":
            self.menu_renderer.display_player_name_input()
            player_name = self.input_handler.handle_player_name_input()

            self.menu_renderer.display_positions_input()
            positions = self.input_handler.handle_positions_input()

            self.menu_renderer.display_colors_input()
            colors = self.input_handler.handle_colors_input()

            self.menu_renderer.display_max_attempts_input()
            max_attempts = self.input_handler.handle_max_attempts_input()

            next_action = self.business_logic.handle_game_mode_choice(
                game_mode, player_name, positions, colors, max_attempts)

        if next_action not in ["back_to_menu", "invalid_mode", "invalid_configuration"]:
            self.handle_game_loop(next_action)




