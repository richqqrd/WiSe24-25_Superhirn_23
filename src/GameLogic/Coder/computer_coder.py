"""Module for computer coder implementation."""

import random
from typing import List

from src.GameLogic.Coder.i_coder import ICoder
from src.util.color_code import ColorCode
from src.util.feedback_color_code import FeedbackColorCode


class ComputerCoder(ICoder):
    """Computer implementation of the coder interface.

    This class represents the computer as code maker. It generates
    secret codes and provides feedback on guesses.

    Attributes:
        positions: Number of positions in the code
        colors: Number of available colors
        __secret_code: The current secret code
    """

    def __init__(self: "ComputerCoder", positions: int, colors: int) -> None:
        """Initialize computer coder with game parameters.

        Args:
            positions: Number of positions in the code
            colors: Number of available colors
        """
        self.__secret_code = []
        self.positions = positions
        self.colors = colors

    def give_feedback(
        self: "ComputerCoder", guess: List[ColorCode]
    ) -> List[FeedbackColorCode]:
        """Provide feedback for a guess.

        Args:
            guess: The guess to evaluate

        Returns:
            List[FeedbackColorCode]: Feedback pins for the guess
        """
        feedback = []

        if len(guess) != self.positions:
            return feedback

        secret_code = self.__secret_code.copy()
        guess_code = guess.copy()

        for i in range(len(secret_code)):
            if guess_code[i] == secret_code[i]:
                feedback.append(FeedbackColorCode.BLACK)
                secret_code[i] = None
                guess_code[i] = None

        for i in range(len(guess_code)):
            if guess_code[i] is not None:
                if guess_code[i] in secret_code:
                    feedback.append(FeedbackColorCode.WHITE)
                    secret_code[secret_code.index(guess_code[i])] = None

        return feedback

    def generate_code(self: "ComputerCoder") -> List[ColorCode]:
        """Generate a random secret code.

        Returns:
            List[ColorCode]: The generated secret code
        """
        self.__secret_code = [
            ColorCode(random.randint(1, self.colors)) for _ in range(self.positions)
        ]
        return self.__secret_code

    @property
    def secret_code(self: "ComputerCoder") -> List[ColorCode]:
        """Get the secret code.

        Returns:
            List[ColorCode]: The current secret code
        """
        return self.__secret_code

    @secret_code.setter
    def secret_code(self: "ComputerCoder", code: List[ColorCode]) -> None:
        """Set the secret code.

        Args:
            code: List of color codes to set as secret code
        """
        self.__secret_code = code
