import pytest
from src.util.FeedbackColorCode import FeedbackColorCode

def test_enum_values():
    """
    Test that the enum values are correctly assigned to the colors.
    """

    assert FeedbackColorCode.WHITE.value == 7
    assert FeedbackColorCode.BLACK.value == 8
