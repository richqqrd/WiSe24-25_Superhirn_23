"""Interface module for coder implementations."""

from abc import ABC, abstractmethod
from typing import List
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class ICoder(ABC):
    """Interface for the coder in the game logic.

    This interface defines the contract for implementing a coder,
    which can be either a human player or computer player that creates
    and evaluates secret codes.

    The coder is responsible for:
        - Generating secret codes
        - Providing feedback on guesses
    """

    @abstractmethod
    def generate_code(self: "ICoder") -> List[ColorCode]:
        """Generate a secret code.

        Returns:
            List[ColorCode]: The generated secret code
        """
        pass

    @abstractmethod
    def give_feedback(self: "ICoder") -> List[FeedbackColorCode]:
        """Provide feedback for a guess.

        Args:
            guess: The guess to evaluate

        Returns:
            List[FeedbackColorCode]: Feedback pins for the guess
        """
        pass
