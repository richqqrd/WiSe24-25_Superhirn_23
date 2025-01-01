from abc import ABC, abstractmethod
from typing import List
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode

class IGameLogic(ABC):
    """Interface for game logic layer."""
    
    @abstractmethod
    def configure_game(self, player_name: str, positions: int, colors: int, max_attempts: int) -> None:
        """Configure the game with initial settings."""
        pass

    @abstractmethod
    def startgame(self, role: str) -> str:
        """Start a new game with the given role."""
        pass

    @abstractmethod
    def set_feedback(self, feedback_list: List[FeedbackColorCode]) -> str:
        """Sets feedback for the current turn."""
        pass

    @abstractmethod
    def get_game_state(self):
        """Returns current game state."""
        pass

    @abstractmethod
    def make_computer_guess(self) -> List[ColorCode]:
        """Let computer make a guess."""
        pass

    @abstractmethod
    def set_secret_code(self, code_list: List[ColorCode]) -> None:
        """Set the secret code for the game."""
        pass

    @abstractmethod
    def make_guess(self, guess_list: List[ColorCode]) -> str:
        """Process a player's guess."""
        pass

    @abstractmethod
    def save_game_state(self) -> None:
        """Save current game state."""
        pass

    @abstractmethod
    def load_game_state(self) -> None:
        """Load saved game state."""
        pass

    @abstractmethod
    def has_saved_game(self) -> bool:
        """Check if there is a saved game."""
        pass

    @abstractmethod
    def is_game_over(self, feedback_list: List[FeedbackColorCode]) -> str:
        """Check if the game is over."""
        pass

    @abstractmethod
    def start_as_online_guesser(self, server_ip: str, server_port: int) -> str:
        """Start game as online guesser."""
        pass