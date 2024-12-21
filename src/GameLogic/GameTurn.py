# src/util/GameTurn.py

from dataclasses import dataclass
from typing import List
from src.util.ColorCode import ColorCode
from src.util.FeedbackColorCode import FeedbackColorCode


@dataclass
class GameTurn:
    """
    Represents a single turn in the game.

    Attributes:
        guesses (List[ColorCode]): The list of color code guesses made by the player.
        feedback (List[FeedbackColorCode]): The list of feedback color codes provided for the guesses.
    """

    guesses: List[ColorCode]
    feedback: List[FeedbackColorCode]
