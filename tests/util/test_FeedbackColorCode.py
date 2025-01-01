# tests/util/test_FeedbackColorCode.py
from src.util.feedback_color_code import FeedbackColorCode


def test_enum_values():
    """
    Test that the enum values are correctly assigned to the colors.
    """
    assert FeedbackColorCode.WHITE.value == 7
    assert FeedbackColorCode.BLACK.value == 8


def test_get_ansi_code():
    """
    Test that the get_ansi_code method returns the correct ANSI color code.
    """
    assert FeedbackColorCode.WHITE.get_ansi_code() == "\033[97m"
    assert FeedbackColorCode.BLACK.get_ansi_code() == "\033[90m"


def test_str_method():
    """
    Test that the __str__ method returns the correct string representation.
    """
    assert str(FeedbackColorCode.WHITE) == "\033[97mWHITE\033[0m"
    assert str(FeedbackColorCode.BLACK) == "\033[90mBLACK\033[0m"
