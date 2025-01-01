import os

from src.BusinessLogic.i_business_logic import IBusinessLogic
from src.GameLogic.i_game_logic import IGameLogic
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.GameLogic.Guesser.player_guesser import PlayerGuesser



class BusinessLogic(IBusinessLogic):
    """
    Concrete implementation of the IBusinessLogic interface.
    """

    def __init__(self, game_logic: IGameLogic):
        """
        Initializes the BusinessLogic instance.
        """
        self.game_logic = game_logic
        self.commands = {
            "1": lambda: "choose_mode",
            "2": lambda: "choose_language",
            "3": lambda: "resume_game",
            "4": lambda: "end_game",
        }

    def handle_game_configuration(self, player_name: str, positions: str, colors: str, max_attempts: str) -> str:
        if not player_name or len(player_name.strip()) == 0:
            return "invalid_configuration"
        
        try:
            pos = int(positions)
            col = int(colors)
            att = int(max_attempts)

            if not (1 <= pos <= 9):
                return "invalid_configuration"
            if not (1 <= col <= 8):
                return "invalid_configuration"
            if att < 0:
                return "invalid_configuration"
            
            return self.game_logic.configure_game(player_name, pos, col, att)
        except ValueError:
            return "invalid_configuration"

    def _is_valid_feedback(self, feedback: str) -> bool:
        try:
            if feedback is None or len(feedback) > 5:
                return False
            if feedback == "" or all(c in "78" for c in feedback):
                return True
            return False
        except Exception:
            return False

    def handle_feedback_input(self, feedback_input: str) -> str:
        if not self._is_valid_feedback(feedback_input):
            return "need_feedback_input"
        try:
            feedback_list = [
                FeedbackColorCode.BLACK if c == "8" else FeedbackColorCode.WHITE
                for c in feedback_input
            ]
            return self.game_logic.set_feedback(feedback_list)
        except ValueError:
            return "need_feedback_input"

    def get_game_state(self):
        return self.game_logic.get_game_state()

    def handle_computer_guess(self) -> str:
        return self.game_logic.make_computer_guess()

    def _is_valid_code(self, code: str) -> bool:
        if not code or len(code) != self.game_logic.positions:
            return False
        try:
            return all(1 <= int(c) <= self.game_logic.colors for c in code)
        except ValueError:
            return False

    def _convert_to_color_code(self, number: int) -> ColorCode:
        """Convert a number to its corresponding ColorCode enum value."""
        for color in ColorCode:
            if color.value == number:  # Jetzt einfacher Vergleich mit Integer
                return color
        raise ValueError(f"No ColorCode found for number {number}")

    def handle_code_input(self, code_input: str) -> str:
        if not self._is_valid_code(code_input):
            return "need_code_input"
        try:
            code_list = [self._convert_to_color_code(int(c)) for c in code_input]
            return self.game_logic.set_secret_code(code_list)
        except ValueError:
            return "need_code_input"

    def handle_guess_input(self, guess_input: str) -> str:
        if not self._is_valid_code(guess_input):
            return "need_guess_input"
        try:
            guess_list = [self._convert_to_color_code(int(g)) for g in guess_input]
            if not guess_list:
                return "need_guess_input"
            return self.game_logic.make_guess(guess_list)
        except ValueError:
            return "need_guess_input"

    def handle(self, command: str) -> str:
        action = self.commands.get(command)
        if action:
            return action()
        else:
            return "Invalid command."

    def handle_server_connection(self, ip: str, port: int) -> str:
        return self.game_logic.start_as_online_guesser(ip, port)

    def change_language(self) -> str:
        return "choose_language"

    def end_game(self) -> str:
        return "end_game"

    def save_game(self) -> str:
        self.game_logic.save_game_state()
        return self.get_current_game_action()

    def load_game(self) -> str:
        try:
            self.game_logic.load_game_state()
            return self.get_current_game_action()
        except FileNotFoundError:
            return "error"

    def process_game_action(self, action: str, user_input: str = None) -> str:
        if action == "need_guess_input":
            if user_input == "menu":
                return "show_menu"
            return self.handle_guess_input(user_input)

        elif action == "need_code_input":
            if user_input == "menu":
                return "show_menu"
            return self.handle_code_input(user_input)

        elif action == "need_feedback_input":
            if user_input == "menu":
                return "show_menu"
            return self.handle_feedback_input(user_input)

        elif action == "wait_for_computer_guess":
            return self.handle_computer_guess()

        elif action == "need_server_connection":
            if user_input == "menu":
                return "show_menu"
            ip, port = user_input.split(":")
            return self.handle_server_connection(ip, int(port))

        return "error"

    def handle_menu_action(self, menu_choice: str) -> str:
        """Handle menu actions based on player role"""
        available_actions = self.get_available_menu_actions()

        menu_map = {
            "1": "save_game" if "save_game" in available_actions else "change_language",
            "2": "change_language" if "save_game" in available_actions else "end_game",
            "3": "load_game" if "load_game" in available_actions else None,
            "4": "end_game" if "save_game" in available_actions else None
        }

        action = menu_map.get(menu_choice)
        if not action:
            return self.get_current_game_action()  # Return to game state

        if action == "save_game":
            if self.game_logic.has_saved_game():
                return "confirm_save"
            self.game_logic.save_game_state()
            return "save_game"
        elif action == "load_game":
            return self.load_game()
        elif action == "change_language":
            return "choose_language"
        elif action == "end_game":
            return "end_game"

        return self.get_current_game_action()






    def get_required_action(self, game_mode: str) -> str:
        if game_mode not in ["1", "2", "3", "4"]:
            return "invalid_mode"

        if game_mode == "4":
            return "back_to_menu"

        return "need_configuration"

    def configure_game(self, game_mode: str, config: dict) -> str:
        config_result = self.handle_game_configuration(
            config["player_name"],
            config["positions"],
            config["colors"],
            config["max_attempts"]
        )

        if config_result == "invalid_configuration":
            return config_result

        if game_mode == "1":
            return self.game_logic.startgame("guesser")

        elif game_mode == "2":
            return self.game_logic.startgame("coder")

        elif game_mode == "3":
            return self.game_logic.startgame("online_guesser")

        return "invalid_mode"

    def can_start_game(self, next_action: str) -> bool:
        return next_action not in ["invalid_mode", "invalid_configuration", "back_to_menu"]
    
    def is_game_over(self, action: str) -> bool:
        return action in ["game_won", "game_lost", "error", "cheating_detected"]

    def get_current_game_action(self) -> str:
        game_state = self.game_logic.get_game_state()
        if isinstance(game_state.current_guesser, PlayerGuesser):
            return "need_guess_input"
        else:
            return "need_feedback_input"

    def get_available_menu_actions(self) -> list[str]:
        """Get available menu actions based on game state"""
        is_guesser = isinstance(self.game_logic.game_state.current_guesser, PlayerGuesser)

        # Common actions
        actions = ["change_language", "end_game"]

        # Guesser-specific actions
        if is_guesser:
            actions.extend(["save_game", "load_game"])

        return actions

    def confirm_save_game(self) -> str:
        """Save game after user confirmed overwrite"""
        try:
            self.game_logic.save_game_state()
            return "save_game"
        except:
            return "error"

    def get_positions(self) -> int:
        """Get number of positions through game logic"""
        game_state = self.game_logic.get_game_state()
        if game_state:
            return game_state.positions
        return self.game_logic.positions

    def get_colors(self) -> int:
        """Get number of positions through game logic"""
        game_state = self.game_logic.get_game_state()
        if game_state:
            return game_state.colors
        return self.game_logic.colors