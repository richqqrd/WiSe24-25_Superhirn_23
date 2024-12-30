import pickle
from src.GameLogic.GameState import GameState

class PersistenceManager:
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
        with open(file_path, "rb") as file:
            return pickle.load(file)