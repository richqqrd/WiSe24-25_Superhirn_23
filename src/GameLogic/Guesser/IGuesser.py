from abc import ABC, abstractmethod
from typing import List
from src.util.ColorCode import ColorCode


class IGuesser(ABC):
    """
    Interface for the guesser in the game logic.
    """

    @abstractmethod
    def make_guess(self) -> List[ColorCode]:
        """
        Makes a guess for the secret code.

        Returns:
            List[ColorCode]: The guessed color code.
        """
        pass
