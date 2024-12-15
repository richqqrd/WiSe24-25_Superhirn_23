from abc import ABC, abstractmethod

class IGameLogic(ABC):
    """
    Interface for the game logic.
    """

    @abstractmethod
    def startGame(self, playerRole: str) -> str:
        """
        Starts the game with the given player role.

        Args:
            playerRole (str): The role of the player (e.g., 'coder' or 'guesser').

        Returns:
            str: The result or state of the game after starting.
        """
        pass