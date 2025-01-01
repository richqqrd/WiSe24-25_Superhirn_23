from abc import ABC, abstractmethod
from src.GameLogic.game_state import GameState

class IPersistenceManager(ABC):
    """Interface for persistence management"""
    
    @abstractmethod
    def save_game_state(self, game_state: GameState, file_path: str = "game_state.pkl") -> None:
        """
        Saves the current game state to a file.

        Args:
            game_state (GameState): The game state to save
            file_path (str): The file path where the game state will be saved

        Raises:
            TypeError: If game_state is not an instance of GameState
        """
        pass

    @abstractmethod
    def load_game_state(self, file_path: str = "game_state.pkl") -> GameState:
        """
        Loads the game state from a file.

        Args:
            file_path (str): The file path from where to load

        Returns:
            GameState: The loaded game state
        """
        pass

    @abstractmethod
    def has_saved_game(self) -> bool:
        """Check if a saved game exists"""
        pass