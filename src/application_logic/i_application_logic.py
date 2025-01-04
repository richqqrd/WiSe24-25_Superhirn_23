"""Interface module for application logic layer."""

from abc import ABC, abstractmethod


class IApplicationLogic(ABC):
    """Interface for application logic layer.

    This interface defines the contract for application logic implementations,
    coordinating game flow and rules between UI and game logic layers.
    """

    @abstractmethod
    def handle(self: "IApplicationLogic", command: str) -> str:
        """Handle general command input.

        Args:
            command: User command to process

        Returns:
            str: Next action to take
        """
        pass

    @abstractmethod
    def handle_game_configuration(
        self: "IApplicationLogic",
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
        pass

    @abstractmethod
    def process_game_action(
        self: "IApplicationLogic", action: str, user_input: str = None
    ) -> str:
        """Process game actions and determine next state.

        Args:
            action: Current game action
            user_input: Optional user input for the action

        Returns:
            str: Next game state
        """
        pass

    @abstractmethod
    def handle_guess_input(self: "IApplicationLogic", guess_input: str) -> str:
        """Handle and validate player guess input.

        Args:
            guess_input: Player's code guess

        Returns:
            str: Result of processing the guess
        """
        pass

    @abstractmethod
    def handle_feedback_input(self: "IApplicationLogic", feedback: str) -> str:
        """Handle and validate feedback input.

        Args:
            feedback: Feedback for last guess

        Returns:
            str: Result of processing the feedback
        """
        pass

    @abstractmethod
    def handle_menu_action(self: "IApplicationLogic", menu_choice: str) -> str:
        """Handle menu actions.

        Args:
            menu_choice: Menu action to process

        Returns:
            str: Result of processing the menu action
        """
        pass

    @abstractmethod
    def get_required_action(self: "IApplicationLogic", game_mode: str) -> str:
        """Get the next required action for a game mode.

        Args:
            game_mode: Current game mode

        Returns:
            str: Next required action for the game mode
        """
        pass

    @abstractmethod
    def configure_game(self: "IApplicationLogic", game_mode: str, config: dict) -> str:
        """Configure a new game with the given mode and settings.

        Args:
            game_mode: Type of game to configure ('guesser', 'coder', 'online')
            config: Dictionary containing game configuration parameters:
                - player_name: Name of the player
                - positions: Number of code positions
                - colors: Number of available colors
                - max_attempts: Maximum allowed attempts

        Returns:
            str: Configuration result status
        """
        pass

    @abstractmethod
    def get_game_state(self) -> "GameState":
        """Get the current game state.

        Returns:
            GameState: Current state of the game
        """
        pass

    @abstractmethod
    def get_positions(self) -> int:
        """Get number of code positions.

        Returns:
            int: Number of positions in the code
        """
        pass

    @abstractmethod
    def get_colors(self) -> int:
        """Get number of available colors.

        Returns:
            int: Number of available colors
        """
        pass

    @abstractmethod
    def get_available_menu_actions(self) -> list:
        """Get list of available menu actions.

        Returns:
            list: List of available menu actions
        """
        pass

    @abstractmethod
    def save_game(self: "IApplicationLogic") -> str:
        """Save the current game state.

        Saves the current game state using the persistence manager.

        Returns:
            str: Save operation result status
        """
        pass

    @abstractmethod
    def load_game(self: "IApplicationLogic") -> str:
        """Load a previously saved game state.

        Loads a saved game state using the persistence manager.

        Returns:
            str: Load operation result status ('error' if no save exists)
        """
        pass

    @abstractmethod
    def can_start_game(self, next_action: str) -> bool:
        """Check if a game can be started with the given action.

        Args:
            next_action: Action to check

        Returns:
            bool: True if game can be started, False otherwise
        """
        pass

    @abstractmethod
    def is_game_over(self, action: str) -> bool:
        """Check if the given action indicates game over.

        Args:
            action: Action to check

        Returns:
            bool: True if game is over, False otherwise
        """
        pass

    @abstractmethod
    def get_current_game_action(self) -> str:
        """Get the current game action based on game state.

        Returns:
            str: Current action needed ("need_guess_input" or "need_feedback_input")
        """
        pass

    @abstractmethod
    def handle_computer_guess(self) -> str:
        """Handle computer making a guess.

        Triggers the computer guesser to make its next move.

        Returns:
            str: Next game state after computer's guess
        """
        pass

    @abstractmethod
    def handle_code_input(self, code_input: str) -> str:
        """Handle and validate secret code input.

        Args:
            code_input: Secret code entered by player

        Returns:
            str: Result of processing the code input
        """
        pass

    @abstractmethod
    def handle_server_connection(self, ip: str, port: int) -> str:
        """Handle online game server connection.

        Args:
            ip: Server IP address
            port: Server port number

        Returns:
            str: Connection result status
        """
        pass

    @abstractmethod
    def change_language(self) -> str:
        """Handle language change request.

        Returns:
            str: "choose_language" to trigger language selection
        """
        pass

    @abstractmethod
    def end_game(self) -> str:
        """Handle game end request.

        Returns:
            str: "end_game" to trigger game ending
        """
        pass

    @abstractmethod
    def confirm_save_game(self) -> str:
        """Handle save game confirmation request.

        Returns:
            str: Next action after save game confirmation
        """
        pass
