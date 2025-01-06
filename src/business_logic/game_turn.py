"""Module for representing a game turn."""

from dataclasses import dataclass
from typing import List
from src.util.color_code import ColorCode # noqa
from src.util.feedback_color_code import FeedbackColorCode # noqa


@dataclass
class GameTurn:
    """Represents a single turn in the game.

    A turn consists of the player's guesses and the corresponding feedback.

    Attributes:
        guesses: List of color code guesses made by the player
        feedback: List of feedback pins indicating correctness of guesses
    """

    guesses: List[ColorCode]
    feedback: List[FeedbackColorCode]
