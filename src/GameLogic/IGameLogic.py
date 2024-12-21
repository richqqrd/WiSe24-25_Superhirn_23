from abc import ABC, abstractmethod
from typing import List

from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class IGameLogic(ABC):
    """
    Interface for the game logic.
    """

    @abstractmethod
    def startgame(self, playerRole: str) -> str:
        """
        Starts the game with the given player role.

        Args:
            playerRole (str): The role of the player (e.g., 'coder' or 'guesser').

        Returns:
            str: The result or state of the game after starting.
        """
        pass

    @abstractmethod
    def start_as_guesser(self) -> str:
        """
        Starts the game as the guesser.

        Returns:
            str: The result or state of the game after starting.
        """
        pass

    @abstractmethod
    def start_as_coder(self) -> str:
        """
        Starts the game as the coder.

        Returns:
            str: The result or state of the game after starting.
        """
        pass

    @abstractmethod
    def set_feedback(self, feedback_list: List[FeedbackColorCode]) -> str:
        """
        Sets the feedback on the current turn.
        """
        pass

    @abstractmethod
    def get_game_state(self):
        """
        Returns the current game state.
        """
        pass

    @abstractmethod
    def make_computer_guess(self):
        """
        Lets the computer make a guess turn.
        """
        pass

    @abstractmethod
    def set_secret_code(self, code_list):
        """
        Sets the coders secret code.
        """
        pass

    @abstractmethod
    def make_guess(self, guess_list: List[ColorCode]) -> str:
        """
        Lets the player make a guess turn.
        """
        pass
