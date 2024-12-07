import pytest
from src.util.ColorCode import ColorCode

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
