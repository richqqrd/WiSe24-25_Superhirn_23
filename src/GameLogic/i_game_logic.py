"""Interface module for game logic layer."""

from abc import ABC, abstractmethod
from typing import List
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class IGameLogic(ABC):
    """Interface for game logic layer.
    
    This interface defines the contract for the game logic implementation,
    handling core game mechanics like:
        - Game configuration
        - Game state management
        - Turn processing
        - Move validation
        - Win/loss conditions
    """

    @abstractmethod
    def configure_game(
        self: "IGameLogic", player_name: str, positions: int, colors: int, max_attempts: int
    ) -> None:
        """Configure the game with initial settings.

        Args:
            player_name: Name of the player
            positions: Number of positions in the code
            colors: Number of available colors
            max_attempts: Maximum number of allowed attempts
        """
        pass

    @abstractmethod
    def startgame(self: "IGameLogic", role: str) -> str:
        """Start a new game with the given role.

        Args:
            role: Player's role ('guesser', 'coder', or 'online_guesser')

        Returns:
            str: Next required action
        """
        pass

    @abstractmethod
    def set_feedback(self: "IGameLogic", feedback_list: List[FeedbackColorCode]) -> str:
        """Sets feedback for the current turn.

        Args:
            feedback_list: List of feedback pins

        Returns:
            str: Next game state
        """        
        pass

    @abstractmethod
    def get_game_state(self: "IGameLogic"):
        """Returns current game state.

        Returns:
            GameState: Current state of the game
        """        
        pass

    @abstractmethod
    def make_computer_guess(self: "IGameLogic") -> List[ColorCode]:
        """Let computer make a guess.

        Returns:
            List[ColorCode]: Computer's guess
        """        
        pass

    @abstractmethod
    def set_secret_code(self: "IGameLogic", code_list: List[ColorCode]) -> None:
        """Set the secret code for the game.

        Args:
            code_list: List of color codes forming the secret code
        """
        pass

    @abstractmethod
    def make_guess(self: "IGameLogic", guess_list: List[ColorCode]) -> str:
        """Process a player's guess.

        Args:
            guess_list: List of color codes representing the guess

        Returns:
            str: Result of the guess
        """
        pass

    @abstractmethod
    def save_game_state(self: "IGameLogic") -> None:
        """Save current game state to persistent storage.
        
        Saves all relevant game information to allow resuming later.
        """
        pass

    @abstractmethod
    def load_game_state(self: "IGameLogic") -> None:
        """Load a previously saved game state.
        
        Restores the game to the state it was in when saved.
        
        Raises:
            FileNotFoundError: If no saved game state exists
        """
        pass

    @abstractmethod
    def has_saved_game(self: "IGameLogic") -> bool:
        """Check if a saved game exists.
        
        Returns:
            bool: True if a saved game exists, False otherwise
        """
        pass

    @abstractmethod
    def is_game_over(self: "IGameLogic", feedback_list: List[FeedbackColorCode]) -> str:
        """Check if the game is over based on feedback.
        
        Args:
            feedback_list: List of feedback pins from last guess
            
        Returns:
            str: Game state ("game_won", "game_lost", or current game state)
        """
        pass

