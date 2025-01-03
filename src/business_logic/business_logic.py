"""Business logic module for game flow control."""
from src.business_logic import business_logic
from src.business_logic.i_business_logic import IBusinessLogic
from src.game_logic.i_game_logic import IGameLogic
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode
from src.game_logic.guesser.player_guesser import PlayerGuesser


class BusinessLogic(IBusinessLogic):
    """Business logic implementation controlling game flow.

    This class coordinates between UI and game logic layers, handling:
        - Command interpretation
        - Input validation
        - Game configuration
        - State transitions

    Attributes:
        game_logic: Core game logic implementation
        commands: Dictionary mapping menu commands to handler functions
    """

    def __init__(self: "business_logic", game_logic: IGameLogic) -> None:
        """Initialize business logic with game logic dependency.

        Args:
            game_logic: Core game logic implementation
        """
        self.game_logic = game_logic
        self.commands = {
            "1": lambda: "choose_mode",
            "2": lambda: "choose_language",
            "3": lambda: "resume_game",
            "4": lambda: "end_game",
        }

    def handle_game_configuration(
            self: "business_logic",
            player_name: str,
            positions: str,
            colors: str,
            max_attempts: str,
    ) -> str:
        """Handle game configuration input validation.

        Args:
            player_name: Name of the player
            positions: Number of code positions
            colors: Number of available colors
            max_attempts: Maximum allowed attempts

        Returns:
            str: Configuration result status
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

            return self.game_logic.configure_game(player_name, pos, col, att)
        except ValueError:
            return "invalid_configuration"

    def _is_valid_feedback(self: "business_logic", feedback: str) -> bool:
        """Validate feedback string format.

        Args:
            feedback: Feedback string to validate

        Returns:
            bool: True if feedback format is valid
        """
        try:
            if feedback is None or len(feedback) > 5:
                return False
            if feedback == "" or all(c in "78" for c in feedback):
                return True
            return False
        except Exception:
            return False

    def handle_feedback_input(self: "business_logic", feedback: str) -> str:
        """Handle and validate feedback input.

        Args:
            feedback: Feedback for last guess

        Returns:
            str: Result of processing the feedback
        """
        if not self._is_valid_feedback(feedback):
            return "need_feedback_input"
        try:
            feedback_list = [
                FeedbackColorCode.BLACK if c == "8" else FeedbackColorCode.WHITE
                for c in feedback
            ]
            return self.game_logic.set_feedback(feedback_list)
        except ValueError:
            return "need_feedback_input"

    def get_game_state(self: "business_logic") -> str:
        """Get the current game state.

        Returns:
            GameState: The current game state
        """
        return self.game_logic.get_game_state()

    def handle_computer_guess(self: "business_logic") -> str:
        """Handle computer making a guess.

        Triggers the computer guesser to make its next move.

        Returns:
            str: Next game state after computer's guess
        """
        return self.game_logic.make_computer_guess()

    def _is_valid_code(self: "business_logic", code: str) -> bool:
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
        if not code or len(code) != self.game_logic.positions:
            return False
        try:
            return all(1 <= int(c) <= self.game_logic.colors for c in code)
        except ValueError:
            return False

    def _convert_to_color_code(self: "business_logic", number: int) -> ColorCode:
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

    def handle_code_input(self: "business_logic", code_input: str) -> str:
        """Handle and validate secret code input.

        Args:
            code_input: Secret code entered by player


        Returns:
            str: Result of processing the code input
        """
        if not self._is_valid_code(code_input):
            return "need_code_input"
        try:
            code_list = [self._convert_to_color_code(int(c)) for c in code_input]
            return self.game_logic.set_secret_code(code_list)
        except ValueError:
            return "need_code_input"

    def handle_guess_input(self: "business_logic", guess_input: str) -> str:
        """Handle and validate guess input.

        Args:
            guess_input: Guess entered by player

        Returns:
            str: Result of processing the guess input
        """
        if not self._is_valid_code(guess_input):
            return "need_guess_input"
        try:
            guess_list = [self._convert_to_color_code(int(g)) for g in guess_input]
            if not guess_list:
                return "need_guess_input"
            return self.game_logic.make_guess(guess_list)
        except ValueError:
            return "need_guess_input"

    def handle(self: "business_logic", command: str) -> str:
        """Handle user command input.

        Args:
            command: Command input from user

        Returns:
            str: Result of processing the command

        Examples:
            "1" -> "choose_mode"
            "2" -> "choose_language"
            "3" -> "resume_game"
            "4" -> "end_game"
        """
        action = self.commands.get(command)
        if action:
            return action()
        else:
            return "Invalid command."

    def handle_server_connection(self: "business_logic", ip: str, port: int) -> str:
        """Handle online game server connection.

        Args:
            ip: Server IP address
            port: Server port number

        Returns:
            str: Connection result status
        """
        return self.game_logic.start_as_online_guesser(ip, port)

    def change_language(self: "business_logic") -> str:
        """Handle language change request.

        Returns:
            str: "choose_language" to trigger language selection
        """
        return "choose_language"

    def end_game(self: "business_logic") -> str:
        """Handle game end request.

        Returns:
            str: "end_game" to end the game
        """
        return "end_game"

    def save_game(self: "business_logic") -> str:
        """Save the current game state.

        Returns:
            str: Next game state after saving
        """
        self.game_logic.save_game_state()
        return self.get_current_game_action()

    def load_game(self: "business_logic") -> str:
        """Load the saved game state.

        Returns:
            str: Next game state after loading
        """
        try:
            self.game_logic.load_game_state()
            return self.get_current_game_action()
        except FileNotFoundError:
            return "error"

    def process_game_action(
            self: "business_logic", action: str, user_input: str = None
    ) -> str:
        """Process the next game action based on user input.

        Args:
            action: The current game action
            user_input: User input for the current action

        Returns:
            str: Next game state after processing the input
        """
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

    def handle_menu_action(self: "business_logic", menu_choice: str) -> str:
        """Handle menu actions.

        Args:
            menu_choice: Menu action to process

        Returns:
            str: Result of processing the menu action
        """
        available_actions = self.get_available_menu_actions()

        menu_map = {
            "1": (
                "save_game" if "save_game" in available_actions else "change_language"
            ),
            "2": "change_language" if "save_game" in available_actions else "end_game",
            "3": "load_game" if "load_game" in available_actions else None,
            "4": "end_game" if "save_game" in available_actions else None,
        }

        action = menu_map.get(menu_choice)
        if not action:
            return self.get_current_game_action()

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

    def get_required_action(self: "business_logic", game_mode: str) -> str:
        """Get the next required action for a game mode.

        Args:
            game_mode: Current game mode

        Returns:
            str: Next game state based on the game mode
        """
        if game_mode not in ["1", "2", "3", "4"]:
            return "invalid_mode"

        if game_mode == "4":
            return "back_to_menu"

        return "need_configuration"

    def configure_game(self: "business_logic", game_mode: str, config: dict) -> str:
        """Configure the game based on user input.

        Args:
            game_mode: The selected game mode
            config: Dictionary containing game configuration settings

        Returns:
            str: Next game state after configuration
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
            return self.game_logic.startgame("guesser")

        elif game_mode == "2":
            return self.game_logic.startgame("coder")

        elif game_mode == "3":
            return self.game_logic.startgame("online_guesser")

        return "invalid_mode"

    def can_start_game(self: "business_logic", next_action: str) -> bool:
        """Check if the game can start based on the next action.

        Args:
            next_action: The next required game action

        Returns:
            bool: True if game can start, False otherwise
        """
        return next_action not in [
            "invalid_mode",
            "invalid_configuration",
            "back_to_menu",
        ]

    def is_game_over(self: "business_logic", action: str) -> bool:
        """Check if the game is over based on the current action.

        Args:
            action: The current game action

        Returns:
            bool: True if game is over, False otherwise
        """
        return action in ["game_won", "game_lost", "error", "cheating_detected"]

    def get_current_game_action(self: "business_logic") -> str:
        """Get the current game action based on game state.

        Returns:
            str: The current game action
        """
        game_state = self.game_logic.get_game_state()
        if isinstance(game_state.current_guesser, PlayerGuesser):
            return "need_guess_input"
        else:
            return "need_feedback_input"

    def get_available_menu_actions(self: "business_logic") -> list[str]:
        """Get the available menu actions based on game state.

        Returns:
            list: List of available menu actions
        """
        is_guesser = isinstance(
            self.game_logic.game_state.current_guesser, PlayerGuesser
        )

        actions = ["change_language", "end_game"]

        if is_guesser:
            actions.extend(["save_game", "load_game"])

        return actions

    def confirm_save_game(self: "business_logic") -> str:
        """Handle save game confirmation.

        Returns:
            str: Next game state after save confirmation
        """
        try:
            self.game_logic.save_game_state()
            return "save_game"
        except Exception:
            return "error"

    def get_positions(self: "business_logic") -> int:
        """Get the number of positions in the game.

        Returns:
            int: Number of positions
        """
        game_state = self.game_logic.get_game_state()
        if game_state:
            return game_state.positions
        return self.game_logic.positions

    def get_colors(self: "business_logic") -> int:
        """Get the number of available colors in the game.

        Returns:
            int: Number of available colors
        """
        game_state = self.game_logic.get_game_state()
        if game_state:
            return game_state.colors
        return self.game_logic.colors
