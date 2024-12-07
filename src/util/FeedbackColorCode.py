# src/util/FeedbackColorCode.py
from enum import Enum


class FeedbackColorCode(Enum):
    """
    Enum representing feedback color codes with their integer values and ANSI codes.
    """

    WHITE = (7, "\033[97m")
    BLACK = (8, "\033[90m")

    def __init__(self, value, ansi_code):
        """
        Initializes the FeedbackColorCode enum instance.

        Args:
            value (int): The integer value representing the color.
            ansi_code (str): The ANSI color code for the color.
        """
        self._value_ = value
        self.ansi_code = ansi_code

    def __str__(self):
        """
        Returns the string representation of the feedback color with the ANSI code.
        Returns:
            str: The feedback color name with the ANSI color code.
        """
        return f"{self.ansi_code}{self.name}\033[0m"

    def get_ansi_code(self):
        """
        Returns the ANSI color code for the feedback color.

        Returns:
            str: The ANSI color code.
        """
        return self.ansi_code
