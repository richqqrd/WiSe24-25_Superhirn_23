from abc import ABC, abstractmethod
from typing import List
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


class ICoder(ABC):
    """
    Interface for the coder in the game logic.
    """

    @abstractmethod
    def generate_code(self) -> List[ColorCode]:
        """
        Generates a secret code.

        Returns:
            List[ColorCode]: The generated secret code.
        """
        pass

    @abstractmethod
    def give_feedback(self) -> List[FeedbackColorCode]:
        """
        Provides feedback for the guesses.

        Returns:
            List[FeedbackColorCode]: The feedback for the guesses.
        """
        pass
