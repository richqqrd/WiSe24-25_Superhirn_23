"""Interface module for guesser implementation."""

from abc import ABC, abstractmethod
from typing import List
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class IGuesser(ABC):
    """Interface for the guesser in the game logic.

    This interface defines the contract for implementing a guesser,
    which can be either a human player or computer player that tries
    to guess the secret code.
    """

    @abstractmethod
    def make_guess(self: "IGuesser") -> List[ColorCode]:
        """Make a guess for the secret code.

        Returns:
            List[ColorCode]: The guessed color code
        """
        pass

    @abstractmethod
    def process_feedback(self: "IGuesser", feedback: List[FeedbackColorCode]) -> None:
        """Process the feedback from the last guess.

        Args:
            feedback: The feedback pins for the last guess
        """
        pass
