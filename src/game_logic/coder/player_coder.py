"""Module for player coder implementation."""

from typing import List

from src.game_logic.coder.i_coder import ICoder
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class PlayerCoder(ICoder):
    """Player implementation of the coder interface.

    This class represents a human player in the coder role. It stores
    the secret code and implements the ICoder interface.

    Attributes:
        code: List of color codes representing the secret code
    """

    def __init__(self: "PlayerCoder"):
        """Initialize player coder with empty code."""
        self.code: List[ColorCode] = []

    def generate_code(self: "PlayerCoder") -> List[ColorCode]:
        if not self.code:
            raise ValueError("Code is not set")
        return self.code

    def give_feedback(self: "PlayerCoder") -> List[FeedbackColorCode]:
        """Give feedback for a guess.

        Not used in player implementation since feedback is provided through input.

        Returns:
            List[FeedbackColorCode]: Empty list as not implemented
        """
        pass
