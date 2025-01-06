"""Module for feedback color code enumeration."""

from enum import Enum


class FeedbackColorCode(Enum):
    """Enum representing feedback color codes with ANSI color codes.

    This enum defines the feedback colors (WHITE, BLACK) used in the game
    along with their corresponding ANSI color codes for terminal display.

    Attributes:
        WHITE: Represents correct color in wrong position (value 7)
        BLACK: Represents correct color in correct position (value 8)
    """

    WHITE = 7
    BLACK = 8

    def __init__(self: "FeedbackColorCode", value: int) -> None:
        """Initialize the FeedbackColorCode enum instance.

        Args:
            value: Integer value for the feedback color (7 or 8)
        """
        self._value_ = value
        # Map values to ANSI codes
        self._ansi_codes = {
            7: "\033[97m",  # WHITE
            8: "\033[90m",  # BLACK
        }
        self.ansi_code = self._ansi_codes[value]

    def __str__(self: "FeedbackColorCode") -> str:
        """Return string representation with ANSI color.

        Returns:
            str: Colored string representation of the enum value
        """
        return f"{self.ansi_code}{self.name}\033[0m"

    def get_ansi_code(self: "FeedbackColorCode") -> str:
        """Get the ANSI color code for this feedback color.

        Returns:
            str: ANSI color code sequence
        """
        return self.ansi_code
