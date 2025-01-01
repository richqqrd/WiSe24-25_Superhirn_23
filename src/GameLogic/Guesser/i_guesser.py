from abc import ABC, abstractmethod
from typing import List
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


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

    @abstractmethod
    def process_feedback(self, feedback: List[FeedbackColorCode]) -> None:
        """
        Processes the feedback from the last guess.

        Args:
            feedback: List[FeedbackColorCode]: The feedback for the last guess
        """
        pass
