"""Application logic module for game flow control."""

from src.business_logic.i_business_logic import IBusinessLogic
from src.application_logic.i_application_logic import IApplicationLogic
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

        # Basic commands that are always available
        self.commands = {
            "1": lambda: "choose_mode",      # Start Game
            "2": lambda: "choose_language",  # Change Language
            "3": lambda: "end_game"         # End Game
        }

        # Add resume_game command only if saved game exists
        if self.business_logic.has_saved_game():
            self.commands = {
                "1": lambda: "choose_mode",
                "2": lambda: "choose_language",
                "3": lambda: "load_game",
                "4": lambda: "end_game"
            }

    def handle_game_configuration(
        self: "ApplicationLogic",
        player_name: str,
        positions: str,
        colors: str,
        max_attempts: str,
    ) -> str:
        """Configure game settings based on user input.

        Args:
            player_name: Name of the player
            positions: Number of positions in the code
            colors: Number of colors available
            max_attempts: Maximum number of attempts allowed

        Returns:
            str: Result of the configuration attempt
        """
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
        """Handle feedback input from the user.

        Args:
            feedback: Feedback string to process

        Returns:
            str: Result of the feedback input
        """
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

    def get_game_state(self: "ApplicationLogic") -> str:
        """Get the current game state.

        Returns:
            str: Current game state
        """
        return self.business_logic.get_game_state()

    def handle_computer_guess(self: "ApplicationLogic") -> str:
        """Handle computer guess in online mode.

        Returns:
            str: Result of the computer guess
        """
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
        """Handle code input from the user.

        Args:
            code_input: Code input string to process

        Returns:
            str: Result of the code input
        """
        if not self._is_valid_code(code_input):
            return "need_code_input"
        try:
            code_list = [self._convert_to_color_code(int(c)) for c in code_input]
            return self.business_logic.set_secret_code(code_list)
        except ValueError:
            return "need_code_input"

    def handle_guess_input(self: "ApplicationLogic", guess_input: str) -> str:
        """Handle guess input from the user.

        Args:
            guess_input: Guess input string to process

        Returns:
            str: Result of the guess input
        """
        if not self._is_valid_code(guess_input):
            return "need_guess_input"
        try:
            guess_list = [self._convert_to_color_code(int(g)) for g in guess_input]
            if not guess_list:
                return "need_guess_input"
            return self.business_logic.make_guess(guess_list)
        except ValueError:
            return "need_guess_input"

    def handle(self: "ApplicationLogic", menu_choice: str) -> str:
        """Handle main menu selection."""
        # Build menu map based on available actions
        available_actions = self.get_available_menu_actions()

        # Basic menu map
        menu_map = {
            "1": "choose_mode",      # Start Game
            "2": "choose_language",  # Change Language
            "3": "end_game"         # End Game
        }

        # Add resume_game if available
        if "load_game" in available_actions:
            menu_map = {
                "1": "choose_mode",
                "2": "choose_language",
                "3": "load_game",
                "4": "end_game"
            }

        return menu_map.get(menu_choice, "invalid")

    def handle_server_connection(self: "ApplicationLogic", ip: str, port: int) -> str:
        """Handle server connection for online mode.

        Args:
            ip: IP address of the server
            port: Port number of the server

        Returns:
            str: Result of the server connection attempt
        """
        if self.business_logic.current_mode == "online_computer_guesser":
            return self.business_logic.start_as_online_computer_guesser(ip, port)
        return self.business_logic.start_as_online_guesser(ip, port)

    def change_language(self: "ApplicationLogic") -> str:
        """Change the game language.

        Returns:
            str: Result of the language change attempt
        """
        return "choose_language"

    def end_game(self: "ApplicationLogic") -> str:
        """End the current game session."""
        return "end_game"

    def save_game(self: "ApplicationLogic") -> str:
        """Save the current game state."""
        self.business_logic.save_game_state()
        return self.get_current_game_action()

    def load_game(self: "ApplicationLogic") -> str:
        """Load the saved game state."""
        try:
            self.business_logic.load_game_state()
            return self.get_current_game_action()
        except FileNotFoundError:
            return "error"

    def process_game_action(self: "ApplicationLogic",
                            action: str, user_input: str = None) -> str:
        """Process the next game action."""
        action_handlers = {
            "need_guess_input": self._handle_guess_action,
            "need_code_input": self._handle_code_action,
            "need_feedback_input": self._handle_feedback_action,
            "wait_for_computer_guess": self._handle_computer_guess_action,
            "need_server_connection": self._handle_server_connection_action
        }

        if action in action_handlers:
            return action_handlers[action](user_input)
        return "error"

    def _handle_guess_action(self: "ApplicationLogic", user_input: str) -> str:
        """Handle guess input action."""
        if user_input == "menu":
            return "show_menu"
        return self.handle_guess_input(user_input)

    def _handle_code_action(self: "ApplicationLogic", user_input: str) -> str:
        """Handle code input action."""
        if user_input == "menu":
            return "show_menu"
        return self.handle_code_input(user_input)

    def _handle_feedback_action(self: "ApplicationLogic", user_input: str) -> str:
        """Handle feedback input action."""
        if user_input == "menu":
            return "show_menu"
        return self.handle_feedback_input(user_input)

    def _handle_computer_guess_action(self: "ApplicationLogic") -> str:
        """Handle computer guess action."""
        result = self.handle_computer_guess()
        return self._process_computer_guess_result(result)

    def _handle_server_connection_action(self: "ApplicationLogic",
                                         user_input: str) -> str:
        """Handle server connection action."""
        if user_input == "menu":
            return "show_menu"

        try:
            ip, port = user_input.split(":")
            return self.handle_server_connection(ip, int(port))
        except ValueError:
            return "need_server_connection"

    def _process_computer_guess_result(self: "ApplicationLogic", result: str) -> str:
        """Process result from computer guess."""
        if result in ["connection_error", "timeout_error"]:
            return "need_server_connection"
        elif result in ["server_error"] or result.startswith("network_error:"):
            return "error"
        return result

    def handle_menu_action(self: "ApplicationLogic", menu_choice: str) -> str:
        """Handle main menu selection.

        Args:
            menu_choice: User input for menu selection

        Returns:
            str: Result of the menu action processing
        """
        available_actions = self.get_available_menu_actions()

        # Baue Menu-Map dynamisch basierend auf verfügbaren Aktionen
        menu_items = []
        if "save_game" in available_actions:
            menu_items.append(("1", "save_game"))
            menu_items.append(("2", "change_language"))
            if "load_game" in available_actions:
                menu_items.append(("3", "load_game"))
                menu_items.append(("4", "back_to_menu"))
                menu_items.append(("5", "end_game"))
            else:
                menu_items.append(("3", "back_to_menu"))
                menu_items.append(("4", "end_game"))
        else:
            menu_items.append(("1", "change_language"))
            menu_items.append(("2", "back_to_menu"))
            menu_items.append(("3", "end_game"))

        # Konvertiere zu Dictionary für Lookup
        menu_map = dict(menu_items)
        action = menu_map.get(menu_choice)

        if not action:
            return self.get_current_game_action()

        # Handle spezifische Aktionen
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
        """Get the required action based on the selected game mode.

        Args:
            game_mode: Selected game mode

        Returns:
            str: Required action based on the game mode
        """
        if game_mode not in ["1", "2", "3", "4", "5"]:
            return "invalid_mode"

        if game_mode == "5":
            return "back_to_menu"

        return "need_configuration"

    def configure_game(self: "ApplicationLogic", game_mode: str, config: dict) -> str:
        """Configure the game based on user input.

        Args:
            game_mode: Selected game mode
            config: Game configuration settings

        Returns:
            str: Result of the game configuration attempt
        """
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
        """Check if the game can be started based on the next action.

        Args:
            next_action: Next action to check

        Returns:
            bool: True if the game can be started, False otherwise
        """
        return next_action not in [
            "invalid_mode",
            "invalid_configuration",
            "back_to_menu",
        ]

    def is_game_over(self: "ApplicationLogic", action: str) -> bool:
        """Check if the game is over based on the current action.

        Args:
            action: Current game action

        Returns:
            bool: True if the game is over, False otherwise
        """
        return action in ["game_won", "game_lost", "error", "cheating_detected"]

    def get_current_game_action(self: "ApplicationLogic") -> str:
        """Get the current game action based on the game state.

        Returns:
            str: Current game action
        """
        game_state = self.business_logic.get_game_state()
        if isinstance(game_state.current_guesser, PlayerGuesser):
            return "need_guess_input"
        else:
            return "need_feedback_input"

    def get_available_menu_actions(self: "ApplicationLogic") -> list[str]:
        """Get the available menu actions based on the current game state.

        Returns:
            list[str]: List of available menu actions
        """
        # Erst prüfen ob game_state existiert
        actions = ["change_language", "end_game"]

        # Im Hauptmenü: Zeige resume_game wenn Spielstand existiert
        if not self.business_logic.game_state:
            if self.business_logic.has_saved_game():
                actions.append("load_game")
            return actions

        is_offline_guesser = (
            isinstance(self.business_logic.game_state.current_guesser, PlayerGuesser)
            and not self.business_logic.network_service
        )
        if is_offline_guesser:
            actions.append("save_game")
            if self.business_logic.has_saved_game():
                actions.append("load_game")

        return actions

    def confirm_save_game(self: "ApplicationLogic") -> str:
        """Confirm the save game action.

        Returns:
            str: Result of the save game confirmation
        """
        try:
            self.business_logic.save_game_state()
            return "save_game"
        except FileNotFoundError:
            return "error"

    def get_positions(self: "ApplicationLogic") -> int:
        """Get the number of positions in the code.

        Returns:
            int: Number of positions in the code
        """
        game_state = self.business_logic.get_game_state()
        if game_state:
            return game_state.positions
        return self.business_logic.positions

    def get_colors(self: "ApplicationLogic") -> int:
        """Get the number of colors available.

        Returns:
            int: Number of colors available
        """
        game_state = self.business_logic.get_game_state()
        if game_state:
            return game_state.colors
        return self.business_logic.colors
