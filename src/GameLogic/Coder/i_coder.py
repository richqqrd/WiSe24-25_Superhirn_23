from abc import ABC, abstractmethod
from typing import List
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


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
