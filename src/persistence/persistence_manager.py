"""Module for managing game state persistence."""

import os
import pickle
from src.game_logic.game_state import GameState
from src.persistence.i_persistence_manager import IPersistenceManager


class PersistenceManager(IPersistenceManager):
    """Manages the persistence of game states.

    This class handles saving and loading game states to/from files.
    Implements the IPersistenceManager interface.

    Attributes:
        save_dir (str): Directory path where game states are saved
    """

    def __init__(self: "PersistenceManager") -> None:
        """Initialize the PersistenceManager.

        Creates the save directory if it doesn't exist.
        """
        self.save_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
        os.makedirs(self.save_dir, exist_ok=True)

    def save_game_state(
        self: "PersistenceManager",
        game_state: GameState,
        file_path: str = "game_state.pkl",
    ) -> None:
        """Save the current game state to a file.

        Args:
            game_state: The game state to save
            file_path: The file path where the game state will be saved

        Raises:
            TypeError: If game_state is not an instance of GameState
        """
        if not isinstance(game_state, GameState):
            raise TypeError("game_state must be an instance of GameState")

        file_path = os.path.join(self.save_dir, file_path)
        with open(file_path, "wb") as file:
            pickle.dump(game_state, file)

    def load_game_state(
        self: "PersistenceManager", file_path: str = "game_state.pkl"
    ) -> GameState:
        """Load a game state from a file.

        Args:
            file_path: The file path from where to load the game state

        Returns:
            GameState: The loaded game state

        Raises:
            FileNotFoundError: If the save file doesn't exist
            pickle.UnpicklingError: If the file contains invalid data
        """
        file_path = os.path.join(self.save_dir, file_path)
        with open(file_path, "rb") as file:
            return pickle.load(file)

    def has_saved_game(self: "PersistenceManager") -> bool:
        """Check if a saved game exists.

        Returns:
            bool: True if a saved game exists, False otherwise
        """
        save_path = os.path.join(self.save_dir, "game_state.pkl")
        return os.path.exists(save_path)
