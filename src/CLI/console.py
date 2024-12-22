from src.BusinessLogic.IBusinessLogic import IBusinessLogic
from src.CLI.game_renderer.game_renderer import GameRenderer
from src.CLI.input_handler.input_handler import InputHandler
from src.CLI.menu_renderer.menu_renderer import MenuRenderer


class Console:
    def __init__(self, business_logic: IBusinessLogic):
        self.business_logic = business_logic
        self.input_handler = InputHandler()
        self.menu_renderer = MenuRenderer()
        self.game_renderer = GameRenderer()
        self.is_game_active = True

    def run(self) -> None:
        while self.is_game_active:
            self.menu_renderer.display_menu()
            user_input = self.input_handler.handle_menu_input()
            next_action = self.business_logic.handle(user_input)

            if next_action == "choose_role_online":
                self.menu_renderer.display_role_menu()
                role_input = self.input_handler.handle_role_input()
                next_action = self.business_logic.handle_role_choice(role_input, "online")
                self.handle_game_loop(next_action)
            elif next_action == "choose_role":
                self.handle_offline_game()
            elif next_action in ["end_game", "save_game", "choose_language"]:
                self.handle_menu_action(next_action)

    def handle_game_loop(self, next_action: str) -> None:
        while next_action not in ["game_over", "error"]:
            if next_action == "need_guess_input":
                self.game_renderer.render_game_state(self.business_logic.get_game_state())
                guess_input = self.input_handler.handle_guess_input()
                next_action = self.business_logic.handle_guess_input(guess_input)
            elif next_action == "need_code_input":
                self.menu_renderer.display_code_input()
                code_input = self.input_handler.handle_code_input()
                next_action = self.business_logic.handle_code_input(code_input)
            elif next_action == "wait_for_computer_guess":
                self.business_logic.handle_computer_guess()
                self.game_renderer.render_game_state(self.business_logic.get_game_state())
                self.menu_renderer.display_feedback_input()
                feedback_input = self.input_handler.handle_feedback_input()
                next_action = self.business_logic.handle_feedback_input(feedback_input)


        if next_action == "game_over":
            self.end_game()
        elif next_action == "error":
            print("Ein Fehler ist aufgetreten. Das Spiel wird beendet.")

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
            self.menu_renderer.display_save_game()
        elif action == "choose_language":
            self.menu_renderer.display_languages()
            self.input_handler.handle_language_input()
        elif action == "end_game":
            self.end_game()