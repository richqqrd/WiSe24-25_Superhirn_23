import pytest
from enum import Enum

class ColorCode(Enum):
    """
    Enum representing various color codes with their respective integer values.
    Provides methods to check if a color is primary or has a rating.
    """
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    ORANGE = 5
    BROWN = 6
    WHITE = 7
    BLACK = 8

def test_enum_values():
    """
    Test that the enum values are correctly assigned to the colors.
    """
    assert ColorCode.RED.value == 1
    assert ColorCode.GREEN.value == 2
    assert ColorCode.YELLOW.value == 3
    assert ColorCode.BLUE.value == 4
    assert ColorCode.ORANGE.value == 5
    assert ColorCode.BROWN.value == 6
    assert ColorCode.WHITE.value == 7
    assert ColorCode.BLACK.value == 8
