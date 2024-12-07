# tests/util/test_ColorCode.py
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

def test_get_ansi_code():
    """
    Test that the get_ansi_code method returns the correct ANSI color code.
    """
    assert ColorCode.RED.get_ansi_code() == "\033[31m"
    assert ColorCode.GREEN.get_ansi_code() == "\033[32m"
    assert ColorCode.YELLOW.get_ansi_code() == "\033[33m"
    assert ColorCode.BLUE.get_ansi_code() == "\033[34m"
    assert ColorCode.ORANGE.get_ansi_code() == "\033[38;5;214m"
    assert ColorCode.BROWN.get_ansi_code() == "\033[38;5;94m"
    assert ColorCode.WHITE.get_ansi_code() == "\033[97m"
    assert ColorCode.BLACK.get_ansi_code() == "\033[90m"


def test_str_method():
    """
    Test that the __str__ method returns the correct string representation.
    """
    assert str(ColorCode.RED) == "\033[31mRED\033[0m"
    assert str(ColorCode.GREEN) == "\033[32mGREEN\033[0m"
    assert str(ColorCode.YELLOW) == "\033[33mYELLOW\033[0m"
    assert str(ColorCode.BLUE) == "\033[34mBLUE\033[0m"
    assert str(ColorCode.ORANGE) == "\033[38;5;214mORANGE\033[0m"
    assert str(ColorCode.BROWN) == "\033[38;5;94mBROWN\033[0m"
    assert str(ColorCode.WHITE) == "\033[97mWHITE\033[0m"
    assert str(ColorCode.BLACK) == "\033[90mBLACK\033[0m"