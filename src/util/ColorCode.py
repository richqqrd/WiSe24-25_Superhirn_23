from enum import Enum


class ColorCode(Enum):
    """
    Enum representing various color codes with their
    respective integer values and ANSI color codes.
    """

    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    ORANGE = 5
    BROWN = 6
    WHITE = 7
    BLACK = 8

    def __init__(self, value):
        """
        Initializes the ColorCode enum instance.
        """
        self._value_ = value
        # Map values to ANSI codes
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

    def __str__(self):
        return f"{self.ansi_code}{self.name}\033[0m"

    def get_ansi_code(self):
        return self.ansi_code
