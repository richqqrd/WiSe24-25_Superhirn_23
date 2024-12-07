# src/util/ColorCode.py
from enum import Enum


class ColorCode(Enum):
    """
    Enum representing various color codes with their respective integer values and ANSI color codes.
    Provides methods to check if a color is primary or has a rating.
    """

    RED = (1, "\033[31m")
    GREEN = (2, "\033[32m")
    YELLOW = (3, "\033[33m")
    BLUE = (4, "\033[34m")
    ORANGE = (5, "\033[38;5;214m")
    BROWN = (6, "\033[38;5;94m")
    WHITE = (7, "\033[97m")
    BLACK = (8, "\033[90m")

    def __init__(self, value, ansi_code):
        """
        Initializes the ColorCode enum instance.

        Args:
            value (int): The integer value representing the color.
            ansi_code (str): The ANSI color code for the color.
        """
        self._value_ = value
        self.ansi_code = ansi_code

    def __str__(self):
        """
        Returns the string representation of the color with the ANSI color code applied.

        Returns:
            str: The color name with the ANSI color code.
        """
        return f"{self.ansi_code}{self.name}\033[0m"

    def get_ansi_code(self):
        """
        Returns the ANSI color code for the color.

        Returns:
            str: The ANSI color code.
        """
        return self.ansi_code
