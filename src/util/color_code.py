"""Module containing color code enumeration for the game."""
from enum import Enum


class ColorCode(Enum):
    """Enum representing various color codes with their respective integer values and ANSI codes.
    
    This enum defines the color codes used in the game along with their corresponding 
    ANSI color codes for terminal display.

    Attributes:
        RED: Red color (value 1)
        GREEN: Green color (value 2)
        YELLOW: Yellow color (value 3)
        BLUE: Blue color (value 4)
        ORANGE: Orange color (value 5)
        BROWN: Brown color (value 6)
        WHITE: White color (value 7)
        BLACK: Black color (value 8)
    """

    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    ORANGE = 5
    BROWN = 6
    WHITE = 7
    BLACK = 8

    def __init__(self: "ColorCode", value: int) -> None:
        """Initialize the ColorCode enum instance.
        
        Args:
            value: Integer value for the color (1-8)
        """
        self._value_ = value
        self._ansi_codes = {
            1: "\033[31m",  # RED
            2: "\033[32m",  # GREEN
            3: "\033[33m",  # YELLOW
            4: "\033[34m",  # BLUE
            5: "\033[38;5;214m",  # ORANGE
            6: "\033[38;5;94m",  # BROWN
            7: "\033[97m",  # WHITE
            8: "\033[90m",  # BLACK
        }
        self.ansi_code = self._ansi_codes[value]

    def __str__(self: "ColorCode") -> str:
        """Return string representation with ANSI color.
        
        Returns:
            str: Colored string representation of the enum value
        """
        return f"{self.ansi_code}{self.name}\033[0m"

    def get_ansi_code(self: "ColorCode") -> str:
        """Get the ANSI color code for this color.
        
        Returns:
            str: ANSI color code sequence
        """
        return self.ansi_code
