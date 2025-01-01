import os
import pickle
from src.GameLogic.game_state import GameState
from src.Persistence.i_persistence_manager import IPersistenceManager


class PersistenceManager(IPersistenceManager):

    def __init__(self):
        self.save_dir = os.path.join(os.path.dirname(__file__), '..', 'saves')
        os.makedirs(self.save_dir, exist_ok=True)




    """
    Manages the persistence of the game state.
    """

    def save_game_state(self, game_state: GameState, file_path: str = "game_state.pkl") -> None:
        """
        Saves the current game state to a file.

        Args:
            game_state (GameState): The game state to save.
            file_path (str): The file path where the game state will be saved.

        Raises:
            TypeError: If the game_state is not an instance of GameState.
        """
        if not isinstance(game_state, GameState):
            raise TypeError("game_state must be an instance of GameState")

        file_path = os.path.join(self.save_dir, file_path)
        with open(file_path, "wb") as file:
            pickle.dump(game_state, file)

    def load_game_state(self, file_path: str = "game_state.pkl") -> GameState:
        """

        Loads the game state from a file.

        Args:
            file_path (str): The file path from where the game state will be loaded.

        Returns:
            GameState: The loaded game state.
        """
        file_path = os.path.join(self.save_dir, file_path)
        with open(file_path, "rb") as file:
            return pickle.load(file)

    def has_saved_game(self) -> bool:
        """Check if a saved game exists"""
        save_path = os.path.join(self.save_dir, "game_state.pkl")
        return os.path.exists(save_path)