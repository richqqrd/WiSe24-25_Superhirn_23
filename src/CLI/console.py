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
            self.menu_renderer.display_main_menu()
            user_input = self.input_handler.handle_menu_input()
            action = self.business_logic.handle(user_input)
            
            if action == "choose_mode":
                self.handle_game_mode_choice()
            elif action == "choose_language":
                self.handle_language_change()
            elif action == "end_game":
                self.end_game()
            elif action  == "save_game":
                self.business_logic.save_game()
                self.menu_renderer.display_save_game()
            elif action == "resume_game":
                next_action = self.business_logic.load_game()
                if next_action != "error":
                    self.start_game_loop(next_action)


    def handle_language_change(self) -> None:
        self.menu_renderer.display_languages()
        language = self.input_handler.handle_language_input(
            self.menu_renderer.language
        )
        self.update_language(language)

    
    def update_language(self, language: str) -> None:
        self.menu_renderer.set_language(language)
        self.game_renderer.set_language(language)
        self.input_handler.set_language(language)



    def start_game_loop(self, next_action: str) -> None:
        """Main game loop controller"""
        while not self.business_logic.is_game_over(next_action):

            if next_action in ["need_guess_input", "need_feedback_input", 
                         "need_code_input", "wait_for_computer_guess"]:
                self.render_game_state()

            user_input = self.get_user_input(next_action)
            next_action = self.business_logic.process_game_action(next_action, user_input)

            if next_action == "show_menu":
                next_action = self.handle_ingame_menu()

        
        self.handle_game_end(next_action)

    def handle_game_end(self, next_action: str) -> None:
        """Handle end of game states"""
        if next_action == "game_over":
            self.game_renderer.render_game_state(
                self.business_logic.get_game_state()
            )
            self.end_game()
        elif next_action == "cheating_detected":
            self.menu_renderer.display_cheating_warning()
            self.end_game()
    
    def render_game_state(self) -> None:
        """Render current game state"""
        self.game_renderer.render_game_state(
            self.business_logic.get_game_state()
        )
            

    def get_user_input(self, action: str) -> str:
        if action == "need_guess_input":
            return self.input_handler.handle_guess_input()

        elif action == "need_code_input":
            return self.input_handler.handle_code_input()

        elif action == "need_feedback_input":
            return self.input_handler.handle_feedback_input()

        elif action == "need_server_connection":
            ip = self.input_handler.handle_ip_input()
            port = self.input_handler.handle_port_input()
            return f"{ip}:{port}"
        return ""





    def handle_ingame_menu(self) -> str:
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


        # Handle UI feedback only
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

    


    def end_game(self) -> None:
        self.menu_renderer.display_end_game()
        self.is_game_active = False

    def handle_game_mode_choice(self) -> None:
        self.menu_renderer.display_game_mode_menu()
        game_mode = self.input_handler.handle_game_mode_input()

        next_action = self.business_logic.get_required_action(game_mode)

        while next_action == "need_configuration":
            config = self.collect_game_configuration()
            next_action = self.business_logic.configure_game(game_mode, config)

        if self.business_logic.can_start_game(next_action):
            self.start_game_loop(next_action)


    def collect_game_configuration(self) -> dict:
        return {
            "player_name": self.input_handler.handle_player_name_input(),
            "positions": self.input_handler.handle_positions_input(),
            "colors": self.input_handler.handle_colors_input(),
            "max_attempts": self.input_handler.handle_max_attempts_input()
        }
