"""Application logic module for game flow control."""

import os
from src.application_logic.i_application_logic import IApplicationLogic
from src.business_logic.i_business_logic import IBusinessLogic
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.business_logic.guesser.player_guesser import PlayerGuesser


class ApplicationLogic(IApplicationLogic):
    """Application logic implementation controlling game flow.

    This class coordinates between UI and game logic layers, handling:
        - Command interpretation
        - Input validation
        - Game configuration
        - State transitions
ƒ
    Attributes:
        business_logic: Core game logic implementation
        commands: Dictionary mapping menu commands to handler functions
    """

    def __init__(self: "ApplicationLogic", business_logic: IBusinessLogic) -> None:
        """Initialize application logic with game logic dependency.

        Args:
            business_logic: Core game logic implementation
        """
        self.business_logic = business_logic
        self.commands = {
            "1": lambda: "choose_mode",
            "2": lambda: "choose_language",
            "3": lambda: "resume_game",
            "4": lambda: "end_game",
        }

    def handle_game_configuration(
        self: "ApplicationLogic",
        player_name: str,
        positions: str,
        colors: str,
        max_attempts: str,
    ) -> str:
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

            return self.business_logic.configure_game(player_name, pos, col, att)
        except ValueError:
            return "invalid_configuration"

    def _is_valid_feedback(self: "ApplicationLogic", feedback: str) -> bool:
        """Validate feedback string format.

        Args:
            feedback: Feedback string to validate

        Returns:
            bool: True if feedback format is valid
        """
        try:
            if feedback is None:
                return False
            if len(feedback) > self.business_logic.positions:
                return False
            if feedback == "" or all(c in "78" for c in feedback):
                return True
            return False
        except Exception:
            return False

    def handle_feedback_input(self: "ApplicationLogic", feedback: str) -> str:
        if not self._is_valid_feedback(feedback):
            return "need_feedback_input"
        try:
            feedback_list = [
                FeedbackColorCode.BLACK if c == "8" else FeedbackColorCode.WHITE
                for c in feedback
            ]
            return self.business_logic.set_feedback(feedback_list)
        except ValueError:
            return "need_feedback_input"

    def get_game_state(self: "ApplicationLogic"):
        return self.business_logic.get_game_state()

    def handle_computer_guess(self: "ApplicationLogic") -> str:
        return self.business_logic.make_computer_guess()

    def _is_valid_code(self: "ApplicationLogic", code: str) -> bool:
        """Validate if a code string meets game requirements.

        Checks if:
        - Code is not empty
        - Code length matches required positions
        - All digits are within valid color range

        Args:
            code: The code string to validate

        Returns:
            bool: True if code is valid, False otherwise
        """
        if not code or len(code) != self.business_logic.positions:
            return False
        try:
            return all(1 <= int(c) <= self.business_logic.colors for c in code)
        except ValueError:
            return False

    def _convert_to_color_code(self: "ApplicationLogic", number: int) -> ColorCode:
        """Convert a number to its corresponding ColorCode enum value.

        Args:
            number: Integer value (1-8) to convert to ColorCode

        Returns:
            ColorCode: Corresponding ColorCode enum value

        Raises:
            ValueError: If no ColorCode exists for the given number

        Examples:
            1 -> ColorCode.RED
            2 -> ColorCode.GREEN
            etc.
        """
        for color in ColorCode:
            if color.value == number:
                return color
        raise ValueError(f"No ColorCode found for number {number}")

    def handle_code_input(self: "ApplicationLogic", code_input: str) -> str:
        if not self._is_valid_code(code_input):
            return "need_code_input"
        try:
            code_list = [self._convert_to_color_code(int(c)) for c in code_input]
            return self.business_logic.set_secret_code(code_list)
        except ValueError:
            return "need_code_input"

    def handle_guess_input(self: "ApplicationLogic", guess_input: str) -> str:
        if not self._is_valid_code(guess_input):
            return "need_guess_input"
        try:
            guess_list = [self._convert_to_color_code(int(g)) for g in guess_input]
            if not guess_list:
                return "need_guess_input"
            return self.business_logic.make_guess(guess_list)
        except ValueError:
            return "need_guess_input"

    def handle(self: "ApplicationLogic", command: str) -> str:
        action = self.commands.get(command)
        if action:
            return action()
        else:
            return "Invalid command."

    def handle_server_connection(self: "ApplicationLogic", ip: str, port: int) -> str:
        if self.business_logic.current_mode == "online_computer_guesser":
            return self.business_logic.start_as_online_computer_guesser(ip, port)
        return self.business_logic.start_as_online_guesser(ip, port)

    def change_language(self: "ApplicationLogic") -> str:
        return "choose_language"

    def end_game(self: "ApplicationLogic") -> str:
        return "end_game"

    def save_game(self: "ApplicationLogic") -> str:
        self.business_logic.save_game_state()
        return self.get_current_game_action()

    def load_game(self: "ApplicationLogic") -> str:
        try:
            self.business_logic.load_game_state()
            return self.get_current_game_action()
        except FileNotFoundError:
            return "error"

    def process_game_action(
        self: "ApplicationLogic", action: str, user_input: str = None
    ) -> str:
        if action == "need_guess_input":
            if user_input == "menu":
                return "show_menu"
            return self.handle_guess_input(user_input)

        elif action == "need_code_input":
            if not self.business_logic.game_state:
                return self.handle_code_input(user_input)
            if user_input == "menu":
                return "show_menu"
            return self.handle_code_input(user_input)

        elif action == "need_feedback_input":
            if user_input == "menu":
                return "show_menu"
            return self.handle_feedback_input(user_input)

        elif action == "wait_for_computer_guess":
            result = self.handle_computer_guess()
                
            if result == "connection_error":
                return "need_server_connection"  # Try reconnecting
            elif result == "server_error":
                return "error"  # Show server error
            elif result == "timeout_error":
                return "need_server_connection"  # Try again
            elif result.startswith("network_error:"):
                return "error"  # Show specific error
                    
            return result

        elif action == "need_server_connection":
            if user_input == "menu":
                return "show_menu"
            try:
                ip, port = user_input.split(":")
                return self.handle_server_connection(ip, int(port))
            except ValueError:
                return "need_server_connection"

        return "error"

    def handle_menu_action(self: "ApplicationLogic", menu_choice: str) -> str:
        available_actions = self.get_available_menu_actions()

        menu_map = {
            "1": ("save_game" if "save_game" in available_actions else "change_language"),
            "2": ("change_language" if "save_game" in available_actions else "back_to_menu"),
            "3": ("load_game" if "load_game" in available_actions else "end_game"),
            "4": ("back_to_menu" if "save_game" in available_actions else None),
            "5": ("end_game" if "save_game" in available_actions else None)
        }

        action = menu_map.get(menu_choice)
        if not action:
            return self.get_current_game_action()

        if action == "save_game":
            if self.business_logic.has_saved_game():
                return "confirm_save"
            self.business_logic.save_game_state()
            return "save_game"
        elif action == "load_game":
            return self.load_game()
        elif action == "change_language":
            return "choose_language"
        elif action == "back_to_menu":
            return "back_to_menu"
        elif action == "end_game":
            return "end_game"

        return self.get_current_game_action()

    def get_required_action(self: "ApplicationLogic", game_mode: str) -> str:
        if game_mode not in ["1", "2", "3", "4", "5"]:
            return "invalid_mode"

        if game_mode == "5":
            return "back_to_menu"

        return "need_configuration"

    def configure_game(self: "ApplicationLogic", game_mode: str, config: dict) -> str:
        config_result = self.handle_game_configuration(
            config["player_name"],
            config["positions"],
            config["colors"],
            config["max_attempts"],
        )

        if config_result == "invalid_configuration":
            return config_result

        if game_mode == "1":
            return self.business_logic.startgame("guesser")

        elif game_mode == "2":
            return self.business_logic.startgame("coder")

        elif game_mode == "3":
            return self.business_logic.startgame("online_guesser")
        
        elif game_mode == "4":
            return self.business_logic.startgame("online_computer_guesser")

        return "invalid_mode"

    def can_start_game(self: "ApplicationLogic", next_action: str) -> bool:
        return next_action not in [
            "invalid_mode",
            "invalid_configuration",
            "back_to_menu",
        ]

    def is_game_over(self: "ApplicationLogic", action: str) -> bool:
        return action in ["game_won", "game_lost", "error", "cheating_detected"]

    def get_current_game_action(self: "ApplicationLogic") -> str:
        game_state = self.business_logic.get_game_state()
        if isinstance(game_state.current_guesser, PlayerGuesser):
            return "need_guess_input"
        else:
            return "need_feedback_input"

    def get_available_menu_actions(self: "ApplicationLogic") -> list[str]:
        # Erst prüfen ob game_state existiert
        if not self.business_logic.game_state:
            return ["change_language", "end_game"]

        is_offline_guesser = (
            isinstance(self.business_logic.game_state.current_guesser, PlayerGuesser) and
            not self.business_logic.network_service
        )

        actions = ["change_language", "end_game"]

        if is_offline_guesser:
            actions.append("save_game")
            if self.business_logic.has_saved_game():
                actions.append("resume_game")

        return actions

    def confirm_save_game(self: "ApplicationLogic") -> str:
        try:
            self.business_logic.save_game_state()
            return "save_game"
        except:
            return "error"

    def get_positions(self: "ApplicationLogic") -> int:
        game_state = self.business_logic.get_game_state()
        if game_state:
            return game_state.positions
        return self.business_logic.positions

    def get_colors(self: "ApplicationLogic") -> int:
        game_state = self.business_logic.get_game_state()
        if game_state:
            return game_state.colors
        return self.business_logic.colors
