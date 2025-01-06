"""Module for player guesser implementation."""

from typing import List

from src.business_logic.guesser.i_guesser import IGuesser # noqa
from src.util.color_code import ColorCode # noqa
from src.util.feedback_color_code import FeedbackColorCode # noqa


class PlayerGuesser(IGuesser):
    """Player implementation of the guesser interface.

    This class represents a human player in the guesser role. It stores
    the current guess and implements the IGuesser interface.

    Attributes:
        current_guess: List of color codes representing the current guess
    """

    def __init__(self: "PlayerGuesser") -> None:
        """Initialize player guesser with empty guess."""
        self.current_guess: List[ColorCode] = []

    def make_guess(self: "PlayerGuesser") -> List[ColorCode]:
        """Return the current guess.

        Returns:
            List[ColorCode]: The current guess
        """
        return self.current_guess

    def set_guess(self: "PlayerGuesser", guess: List[ColorCode]) -> None:
        """Set the current guess.

        Args:
            guess: List of color codes to set as current guess
        """
        self.current_guess = guess if guess is not None else []

    def process_feedback(
        self: "PlayerGuesser", feedback: List[FeedbackColorCode]
    ) -> None:
        """Process feedback from last guess.

        Not used in player implementation since player makes own decisions.

        Args:
            feedback: Feedback from last guess
        """
        pass
