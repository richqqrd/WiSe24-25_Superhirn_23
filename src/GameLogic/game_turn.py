# src/util/game_turn.py

from dataclasses import dataclass
from typing import List
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


@dataclass
class GameTurn:
    """
    Represents a single turn in the game.

    Attributes:
        guesses (List[ColorCode]): The list of color code guesses made
        by the player.
        feedback (List[FeedbackColorCode]): The list of feedback color
        codes provided for the guesses.
    """

    guesses: List[ColorCode]
    feedback: List[FeedbackColorCode]
