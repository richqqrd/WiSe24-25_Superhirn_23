# src/util/FeedbackColorCode.py
from enum import Enum

class FeedbackColorCode(Enum):
    """
    Enum representing feedback color codes with their respective integer values and ANSI color codes.
    """

    WHITE = 7
    BLACK = 8

    def __init__(self, value):
        """
        Initializes the FeedbackColorCode enum instance.
        """
        self._value_ = value
        # Map values to ANSI codes
        self._ansi_codes = {
            7: "\033[97m",  # WHITE
            8: "\033[90m",  # BLACK
        }
        self.ansi_code = self._ansi_codes[value]

    def __str__(self):
        return f"{self.ansi_code}{self.name}\033[0m"

    def get_ansi_code(self):
        return self.ansi_code