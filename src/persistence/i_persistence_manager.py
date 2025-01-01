from abc import ABC, abstractmethod
from src.game_logic.game_state import GameState


class IPersistenceManager(ABC):
    """Interface for persistence management.

    This interface defines the contract for managing game state persistence,
    including saving and loading game states.
    """

    @abstractmethod
    def save_game_state(
        self: "IPersistenceManager",
        game_state: GameState,
        file_path: str = "game_state.pkl",
    ) -> None:
        """Save the current game state to a file.

        Args:
            game_state: The game state to save
            file_path: The file path where the game state will be saved.
                      Defaults to "game_state.pkl"

        Raises:
            TypeError: If game_state is not an instance of GameState
        """
        pass

    @abstractmethod
    def load_game_state(
        self: "IPersistenceManager", file_path: str = "game_state.pkl"
    ) -> GameState:
        """Load the game state from a file.

        Args:
            file_path: The file path from where to load.
                      Defaults to "game_state.pkl"

        Returns:
            GameState: The loaded game state

        Raises:
            FileNotFoundError: If the save file doesn't exist
            pickle.UnpicklingError: If the file contains invalid data
        """
        pass

    @abstractmethod
    def has_saved_game(self: "IPersistenceManager") -> bool:
        """Check if a saved game exists.

        Returns:
            bool: True if a saved game exists, False otherwise
        """
        pass
